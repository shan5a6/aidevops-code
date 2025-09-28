import streamlit as st
import os
import re
import subprocess
import shlex

st.set_page_config(page_title="Day 12+: Advanced Terraform Module Generator & Validator", layout="wide")

st.title("🚀 Day 12+: Advanced Terraform Import Splitter — Combined main.tf")

# Config: Terraformer output folder
TERRAFORMER_OUTPUT_DIR = "/root/tf-import/generated/aws"

RESOURCE_MODULE_MAP = {
    "aws_vpc": "vpc",
    "aws_subnet": "vpc",
    "aws_security_group": "vpc",
    "aws_instance": "ec2",
    "aws_db_instance": "rds",
}


def extract_resource_blocks(tf_text):
    blocks = []
    stack = []
    start_idx = None
    for i, c in enumerate(tf_text):
        if tf_text[i:i + 8] == 'resource':
            if start_idx is None:
                start_idx = i
            stack = []
        if start_idx is not None:
            if c == '{':
                stack.append(c)
            elif c == '}':
                if stack:
                    stack.pop()
                if not stack:
                    blocks.append(tf_text[start_idx:i + 1].strip())
                    start_idx = None
    return blocks


def detect_resource_type_and_name(block):
    m = re.match(r'resource\s+"([^"]+)"\s+"([^"]+)"', block)
    if m:
        return m.group(1), m.group(2)
    return None, None


def normalize_block(s):
    return re.sub(r"\s+", " ", s).strip()


def append_unique_block(path, block):
    """
    Append block to main.tf if not already present.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    new_block = normalize_block(block)

    if os.path.exists(path):
        with open(path, "r") as f:
            existing = f.read()
        existing_blocks = extract_resource_blocks(existing)
        for eb in existing_blocks:
            if normalize_block(eb) == new_block:
                return False  # Already exists

    with open(path, "a") as f:
        if os.path.getsize(path) > 0:
            f.write("\n\n")
        f.write(block.strip() + "\n")
    return True


def write_file_safely(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)


def generate_variables_tf(blocks):
    var_lines = []
    for block in blocks:
        for line in block.splitlines():
            line = line.strip()
            if line.startswith("resource") or line.startswith("}"):
                continue
            if "=" in line:
                key = line.split("=")[0].strip()
                if key in ["resource", "name", "tags"]:
                    continue
                var_lines.append(f'variable "{key}" {{\n  type = string\n}}\n')
    return "\n".join(var_lines)


def generate_outputs_tf(blocks):
    outputs = []
    for block in blocks:
        rtype, rname = detect_resource_type_and_name(block)
        if not rtype or not rname:
            continue
        outputs.append(f'output "{rname}_id" {{\n  value = {rtype}.{rname}.id\n}}\n')
        if rtype == "aws_instance":
            outputs.append(f'output "{rname}_public_ip" {{\n  value = {rtype}.{rname}.public_ip\n}}\n')
        if rtype == "aws_vpc":
            outputs.append(f'output "{rname}_cidr_block" {{\n  value = {rtype}.{rname}.cidr_block\n}}\n')
    return "\n".join(outputs)


def terraform_command(module_dir, command):
    try:
        result = subprocess.run(
            ["terraform"] + shlex.split(command),
            cwd=module_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False
        )
        return result.stdout
    except Exception as e:
        return f"Error running terraform {command}: {e}"


st.markdown(f"### Reading Terraform files from: `{TERRAFORMER_OUTPUT_DIR}`")

if not os.path.exists(TERRAFORMER_OUTPUT_DIR):
    st.error(f"Folder `{TERRAFORMER_OUTPUT_DIR}` not found!")
    st.stop()

tf_files = []
for root, dirs, files in os.walk(TERRAFORMER_OUTPUT_DIR):
    for file in files:
        if file.endswith(".tf"):
            tf_files.append(os.path.relpath(os.path.join(root, file), TERRAFORMER_OUTPUT_DIR))

if not tf_files:
    st.warning("No `.tf` files found in the Terraformer output folder.")
    st.stop()

selected_file = st.selectbox("Select a Terraform file to process:", tf_files)

full_file_path = os.path.join(TERRAFORMER_OUTPUT_DIR, selected_file)
with open(full_file_path, "r") as f:
    tf_content = f.read()

resource_blocks = extract_resource_blocks(tf_content)
st.markdown(f"### Detected {len(resource_blocks)} resource blocks in `{selected_file}`")

edited_blocks = []
for i, block in enumerate(resource_blocks):
    rtype, rname = detect_resource_type_and_name(block)
    st.markdown(f"#### Resource Block #{i + 1} — `{rtype}` `{rname}`")
    edited_code = st.text_area(
        f"Edit resource block #{i + 1}",
        value=block,
        height=200,
        key=f"block_{i}"
    )
    edited_blocks.append((edited_code, rtype, rname))

if st.button("💾 Save all blocks to combined main.tf per module"):
    for block, rtype, rname in edited_blocks:
        if not rtype or not rname:
            st.warning(f"Skipped block with unknown type/name")
            continue

        module_folder = RESOURCE_MODULE_MAP.get(rtype, "misc")
        module_dir = os.path.join("modules", module_folder)
        main_tf_path = os.path.join(module_dir, "main.tf")

        saved = append_unique_block(main_tf_path, block)
        if saved:
            st.success(f"✅ Added `{rname}` to `{main_tf_path}`")
        else:
            st.info(f"ℹ️ `{rname}` already exists in `{main_tf_path}`, skipped.")

        # Update variables.tf and outputs.tf
        variables_content = generate_variables_tf([b for b, _, _ in edited_blocks])
        write_file_safely(os.path.join(module_dir, "variables.tf"), variables_content)

        outputs_content = generate_outputs_tf([b for b, _, _ in edited_blocks])
        write_file_safely(os.path.join(module_dir, "outputs.tf"), outputs_content)

        subprocess.run(["terraform", "fmt"], cwd=module_dir)

        st.markdown(f"### Running terraform init & validate in `{module_dir}` ...")
        init_out = terraform_command(module_dir, "init -input=false -no-color")
        st.code(init_out, language="bash")
        validate_out = terraform_command(module_dir, "validate -no-color")
        st.code(validate_out, language="bash")

    st.success("✅ All blocks processed!")

st.markdown("---")
st.markdown("### Optional: Run terraform plan on a module")

plan_module = st.selectbox("Select module to plan:", ["-- Select --"] + list(set(RESOURCE_MODULE_MAP.values())))
if plan_module != "-- Select --":
    module_dir = os.path.join("modules", plan_module)
    if st.button(f"▶️ Run terraform plan in `{plan_module}`"):
        plan_output = terraform_command(module_dir, "plan -no-color")
        st.code(plan_output, language="bash")
