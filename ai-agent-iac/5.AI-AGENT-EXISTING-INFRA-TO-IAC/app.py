# """
# Streamlit Terraform Module Merger + GROQ assistant
# - Reads existing generated/aws/vpc and generated/aws/subnet TF files
# - Aggregates them into a single module
# - Sends them to a GROQ LLM for refinement (if configured)
# - Shows result on full-width UI; user can review/edit and save
# - Runs terraform fmt -recursive on the saved folder (optional)
# """

# import os
# import glob
# import shutil
# import subprocess
# import textwrap
# import json
# from typing import Dict, Tuple, List

# import streamlit as st

# from dotenv import load_dotenv
# load_dotenv()

# # Optional: requests only required if using GROQ API
# try:
#     import requests
# except Exception:
#     requests = None

# # ---------------------------
# # Configuration (change if needed)
# # ---------------------------
# ROOT_GENERATED = "/root/tf-import/generated/aws"
# COMBINED_MODULE_DIR = os.path.join(ROOT_GENERATED, "combined_module")
# VPC_DIR = os.path.join(ROOT_GENERATED, "vpc")
# SUBNET_DIR = os.path.join(ROOT_GENERATED, "subnet")

# # GROQ API config (set as environment variables for real usage)
# GROQ_API_KEY = os.environ.get("GROQ_API_KEY")  # None -> fallback to local merger
# GROQ_API_URL = os.environ.get("GROQ_API_URL", "https://api.groq.example/v1/generate")


# # ---------------------------
# # Utility functions
# # ---------------------------
# def read_tf_files_from_dir(directory: str) -> Dict[str, str]:
#     """
#     Read all .tf and .tfvars files in a directory and return mapping filename->content.
#     """
#     data = {}
#     if not os.path.isdir(directory):
#         return data
#     patterns = ["*.tf", "*.tfvars", "*.tf.json"]
#     for pat in patterns:
#         for path in sorted(glob.glob(os.path.join(directory, pat))):
#             name = os.path.basename(path)
#             with open(path, "r", encoding="utf-8") as f:
#                 data[name] = f.read()
#     return data


# def aggregate_module_payload(vpc_files: Dict[str, str], subnet_files: Dict[str, str]) -> str:
#     """
#     Produce a single text payload combining given files with simple section markers.
#     This payload will be sent to the LLM for refinement.
#     """
#     sections = []
#     sections.append("# === VPC Files ===")
#     for fn, content in vpc_files.items():
#         sections.append(f"# -- {fn} --")
#         sections.append(content.strip())

#     sections.append("\n# === SUBNET Files ===")
#     for fn, content in subnet_files.items():
#         sections.append(f"# -- {fn} --")
#         sections.append(content.strip())

#     # include a human instruction for the LLM
#     instruction = textwrap.dedent(
#         """
#         ##
#         ## Instruction:
#         ## - Combine the VPC and Subnet TF fragments into a single, well-formed Terraform module.
#         ## - Remove duplicate provider blocks, consolidate variables and outputs.
#         ## - Ensure resources have consistent names and references.
#         ## - Return final working terraform code only (no commentary).
#         ##
#         """
#     )
#     payload = "\n\n".join([instruction] + sections)
#     return payload


# from groq import Groq

# # Initialize client
# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# # Example call
# response = client.chat.completions.create(
#     model="llama-3.3-70b-versatile",  # or any supported model
#     messages=[
#         {"role": "system", "content": "You are a Terraform refactoring assistant."},
#         {"role": "user", "content": "Combine subnet and VPC modules into one clean Terraform module."}
#     ]
# )

# print(response.choices[0].message["content"])

# def call_groq_api(prompt: str, api_key: str = None, api_url: str = None, timeout: int = 30) -> Tuple[bool, str]:
#     """
#     Call the GROQ LLM API. Returns (success, text).
#     This is a sample placeholder; adapt headers/payload to your GROQ contract.
#     If requests isn't installed or api_key is not set, returns failure.
#     """
#     if requests is None or api_key is None:
#         return False, "GROQ not configured or 'requests' not installed."

#     headers = {
#         "Authorization": f"Bearer {api_key}",
#         "Content-Type": "application/json",
#     }
#     payload = {
#         "prompt": prompt,
#         # The real GROQ API may expect different fields; adapt as required.
#         "max_tokens": 4000,
#         "temperature": 0.0,
#     }
#     try:
#         resp = requests.post(api_url, headers=headers, json=payload, timeout=timeout)
#         resp.raise_for_status()
#         body = resp.json()
#         # Adapt depending on response schema. We'll try common shapes:
#         if "text" in body:
#             return True, body["text"]
#         if "choices" in body and isinstance(body["choices"], list) and len(body["choices"]) > 0:
#             text = body["choices"][0].get("text") or body["choices"][0].get("message", {}).get("content", "")
#             return True, text
#         # fallback: return full body as string
#         return True, json.dumps(body, indent=2)
#     except Exception as e:
#         return False, f"Error calling GROQ API: {str(e)}"


# def local_fallback_refine_combination(payload: str) -> str:
#     """
#     A safe, deterministic fallback that tries to:
#     - Remove duplicate provider blocks
#     - Concatenate unique variable blocks
#     - Put resources from input in a single file with simple separators
#     This is NOT a real LLM rewrite but useful when GROQ isn't available.
#     """
#     lines = payload.splitlines()
#     out_lines = []
#     seen_provider = False
#     # crude removal of duplicate provider blocks (simple heuristic)
#     in_provider = False
#     in_variable = False
#     variables = {}
#     outputs = []
#     resources = []
#     other = []

#     current_block = []
#     current_block_type = None

#     def flush_block():
#         nonlocal current_block, current_block_type
#         text = "\n".join(current_block).strip()
#         if not text:
#             current_block = []
#             current_block_type = None
#             return
#         if current_block_type == "variable":
#             # key is variable name - find "variable \"name\""
#             for line in current_block:
#                 if line.strip().startswith('variable '):
#                     name = line.strip().split()[1].strip().strip('"')
#                     variables[name] = text
#                     break
#         elif current_block_type == "output":
#             outputs.append(text)
#         elif current_block_type == "resource":
#             resources.append(text)
#         else:
#             other.append(text)
#         current_block = []
#         current_block_type = None

#     for line in lines:
#         stripped = line.strip()
#         if stripped.startswith("provider "):
#             # skip repeating provider blocks; keep first
#             if not seen_provider:
#                 seen_provider = True
#                 out_lines.append(line)
#             in_provider = True
#             continue
#         if in_provider:
#             # heuristic end of provider block: blank line or 'resource' or 'variable' or 'output'
#             if stripped == "" or stripped.startswith("resource ") or stripped.startswith("variable ") or stripped.startswith("output "):
#                 in_provider = False
#             else:
#                 # include provider inner lines only for first provider
#                 if seen_provider and out_lines and out_lines[-1].strip().startswith("provider "):
#                     out_lines.append(line)
#                 continue

#         # classify blocks: variable, output, resource
#         if stripped.startswith('variable '):
#             flush_block()
#             current_block = [line]
#             current_block_type = "variable"
#             continue
#         if stripped.startswith('output '):
#             flush_block()
#             current_block = [line]
#             current_block_type = "output"
#             continue
#         if stripped.startswith('resource '):
#             flush_block()
#             current_block = [line]
#             current_block_type = "resource"
#             continue

#         # accumulate continuing lines in current block if any
#         if current_block_type:
#             current_block.append(line)
#         else:
#             other.append(line)

#     flush_block()

#     # Build single-file module
#     result_parts = []
#     result_parts.append("# Combined module produced by local fallback")
#     if out_lines:
#         # Keep provider of first file if present
#         result_parts.append("\n".join(out_lines))

#     # Variables
#     if variables:
#         result_parts.append("\n\n# Variables")
#         for v in variables.values():
#             result_parts.append(v)

#     # Other top-level content
#     if other:
#         result_parts.append("\n\n# Other top-level content\n")
#         result_parts.append("\n".join(other))

#     # Resources
#     if resources:
#         result_parts.append("\n\n# Resources (combined)\n")
#         for r in resources:
#             result_parts.append(r)

#     # Outputs
#     if outputs:
#         result_parts.append("\n\n# Outputs\n")
#         for o in outputs:
#             result_parts.append(o)

#     return "\n\n".join(result_parts)


# def save_generated_code(code: str, dest_dir: str) -> Tuple[bool, str]:
#     """
#     Save generated code as main.tf in the destination directory.
#     Returns (success, message).
#     """
#     try:
#         os.makedirs(dest_dir, exist_ok=True)
#         file_path = os.path.join(dest_dir, "main.tf")
#         with open(file_path, "w", encoding="utf-8") as f:
#             f.write(code.strip() + "\n")
#         return True, file_path
#     except Exception as e:
#         return False, str(e)


# def run_terraform_fmt(directory: str) -> Tuple[bool, str]:
#     """
#     Run terraform fmt -recursive on the given directory if terraform exists.
#     Returns (success, output).
#     """
#     try:
#         res = subprocess.run(
#             ["terraform", "fmt", "-recursive"],
#             cwd=directory,
#             capture_output=True,
#             text=True,
#             check=False,
#         )
#         out = res.stdout.strip()
#         err = res.stderr.strip()
#         result = "\n".join([out, err]).strip()
#         if res.returncode == 0:
#             return True, result or "Formatted successfully or no changes."
#         else:
#             return False, result or f"terraform fmt returned code {res.returncode}"
#     except FileNotFoundError:
#         return False, "terraform binary not found on this system."
#     except Exception as e:
#         return False, str(e)


# # ---------------------------
# # Streamlit UI
# # ---------------------------

# st.set_page_config(page_title="Terraform Module Merger (IaC Agent)", layout="wide")
# st.title("🧩 Terraform Module Merger — IaC Agent")

# st.markdown(
#     """
#     This tool reads your `generated/aws/vpc` and `generated/aws/subnet` TF fragments,
#     asks the GROQ LLM (or uses a local fallback) to **refine & combine** them into a single
#     module, and lets you preview & confirm saving the result.
#     """
# )

# # --- Left: source explorer / options ---
# left_col, right_col = st.columns([1, 3])  # small left panel + large right panel

# with left_col:
#     st.header("Source files")
#     st.write(f"Root generated folder: `{ROOT_GENERATED}`")

#     if not os.path.isdir(ROOT_GENERATED):
#         st.error(f"Root generated path '{ROOT_GENERATED}' not found on disk.")
#     else:
#         # list tree for vpc and subnet
#         def show_dir_tree(path):
#             if not os.path.isdir(path):
#                 st.write(f"- `{path}` not found")
#                 return
#             st.write(f"**{os.path.basename(path)}/**")
#             paths = sorted(glob.glob(os.path.join(path, "*")))
#             for p in paths:
#                 name = os.path.basename(p)
#                 if os.path.isdir(p):
#                     st.write(f"- {name}/")
#                 else:
#                     st.write(f"- {name}")

#         show_dir_tree(VPC_DIR)
#         show_dir_tree(SUBNET_DIR)

#     st.markdown("---")
#     st.subheader("Options")
#     module_name = st.text_input("Module name to create:", value="combined_module")
#     dest_dir = st.text_input("Destination folder:", value=COMBINED_MODULE_DIR)
#     show_run_fmt = st.checkbox("Run `terraform fmt -recursive` after save", value=True)

#     st.markdown("### GROQ / LLM")
#     st.write("If you want to use a real GROQ endpoint, set `GROQ_API_KEY` & `GROQ_API_URL` in env.")
#     groq_enabled = bool(GROQ_API_KEY)
#     st.write(f"GROQ enabled: {groq_enabled}")

# # --- Right: main action area (full width outputs) ---
# with right_col:
#     st.header("Merge & Refine")

#     # Read files into variables
#     vpc_files = read_tf_files_from_dir(VPC_DIR)
#     subnet_files = read_tf_files_from_dir(SUBNET_DIR)

#     st.subheader("Preview inputs (concatenated)")
#     example_payload = aggregate_module_payload(vpc_files, subnet_files)
#     # show a shortened preview to avoid huge rendering; user can expand via expander
#     with st.expander("Show concatenated input payload for LLM (click to expand)", expanded=False):
#         st.code(example_payload[:4000] + ("\n\n... (truncated)" if len(example_payload) > 4000 else ""), language="hcl")

#     st.markdown("### Provide any extra instruction for the LLM (optional)")
#     user_extra_instruction = st.text_area("Extra instruction:", value="Combine and return final terraform module only.", height=80)

#     # Buttons row (full width output shown below)
#     bcol1, bcol2, bcol3 = st.columns([1, 1, 1])

#     generate_clicked = bcol1.button("Generate (LLM)")
#     preview_local_clicked = bcol2.button("Local Combine (no LLM)")
#     refresh_clicked = bcol3.button("Refresh Source Files")

#     # Variables to hold outputs
#     generated_code = None
#     generation_meta = {}

#     if refresh_clicked:
#         # re-read
#         vpc_files = read_tf_files_from_dir(VPC_DIR)
#         subnet_files = read_tf_files_from_dir(SUBNET_DIR)
#         st.success("Refreshed file list.")
#         st.experimental_rerun()

#     if generate_clicked:
#         st.info("Calling GROQ LLM to refine & combine the module. This may take a moment...")
#         payload = aggregate_module_payload(vpc_files, subnet_files)
#         if user_extra_instruction:
#             payload = user_extra_instruction + "\n\n" + payload

#         success, result_text = call_groq_api(payload, api_key=GROQ_API_KEY, api_url=GROQ_API_URL)
#         if success:
#             generated_code = result_text.strip()
#             generation_meta["source"] = "groq"
#             st.success("GROQ generation complete.")
#         else:
#             # Show error but also fall back to local combination
#             st.error(f"GROQ failed: {result_text}")
#             st.info("Falling back to local combine.")
#             generated_code = local_fallback_refine_combination(payload)
#             generation_meta["source"] = "local_fallback"

#     if preview_local_clicked:
#         st.info("Combining files locally (no network calls).")
#         payload = aggregate_module_payload(vpc_files, subnet_files)
#         if user_extra_instruction:
#             payload = user_extra_instruction + "\n\n" + payload
#         generated_code = local_fallback_refine_combination(payload)
#         generation_meta["source"] = "local_fallback"
#         st.success("Local combination ready.")

#     # If we have a generated result, show full-width output below the buttons
#     if generated_code:
#         st.markdown("## Generated / Refined Module (preview)")
#         st.write(f"**Generated by:** {generation_meta.get('source')}")
#         # Allow editing inline
#         edited_code = st.text_area("Edit or review the generated code (this text will be saved):", value=generated_code, height=520)

#         # Save / discard
#         save_col1, save_col2 = st.columns([1, 1])
#         with save_col1:
#             if st.button("Save module to disk"):
#                 # capture and assign variables that must be visible
#                 user_prompt = user_extra_instruction
#                 root_path = ROOT_GENERATED
#                 module_target = dest_dir

#                 success, message = save_generated_code(edited_code, dest_dir)
#                 if success:
#                     st.success(f"Saved generated module to {message}")
#                     # run terraform fmt optionally
#                     if show_run_fmt:
#                         ok, fmt_out = run_terraform_fmt(dest_dir)
#                         if ok:
#                             st.info("terraform fmt output:")
#                             st.code(fmt_out or "No output")
#                         else:
#                             st.warning(f"terraform fmt issues: {fmt_out}")

#                     # Print captured inputs/variables on page
#                     st.markdown("### Captured Variables (for transparency)")
#                     st.write("**module_name**:", module_name)
#                     st.write("**module_target (dest_dir)**:", module_target)
#                     st.write("**user_extra_instruction**:", user_prompt)
#                     st.write("**root_path**:", root_path)
#                     st.write("**generation_source**:", generation_meta.get("source"))
#                     st.write("**saved_file**:", message)

#                 else:
#                     st.error(f"Failed to save: {message}")

#         with save_col2:
#             if st.button("Discard / Do not save"):
#                 st.warning("Generation discarded. Nothing saved to disk.")
#                 # show captured inputs
#                 st.markdown("### Captured Variables (discard action)")
#                 st.write("**module_name**:", module_name)
#                 st.write("**dest_dir**:", dest_dir)
#                 st.write("**user_extra_instruction**:", user_extra_instruction)

#     else:
#         st.info("No generated module yet. Use 'Generate (LLM)' or 'Local Combine (no LLM)' to create.")

# # Footer / tips
# st.markdown("---")
# st.write(
#     """
#     **Tips**
#     - To enable GROQ: set `GROQ_API_KEY` and `GROQ_API_URL` environment variables.
#     - This tool provides a preview. Always review generated TF before applying.
#     """
# )
