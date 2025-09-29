def contentparsing(response: str):
    import re, os, shutil

    # Base directory for generated Terraform code
    TERRAFORM_DIR = os.path.join(os.getcwd(), "terraform")

    # Optional: Clean existing terraform dir before writing new files
    if os.path.exists(TERRAFORM_DIR):
        shutil.rmtree(TERRAFORM_DIR)
    os.makedirs(TERRAFORM_DIR, exist_ok=True)

    # Regex to detect cloud sections (### AWS: modules/aws/, ### Azure: modules/azure/, etc.)
    cloud_section_pattern = r"###\s*(\w+):\s*(modules/[^\n/]+/)"
    cloud_sections = re.split(cloud_section_pattern, response)

    if len(cloud_sections) <= 1:
        print("⚠️ No cloud sections found. Falling back to single parser.")
        return _single_cloud_parser(response, TERRAFORM_DIR)

    # cloud_sections will split into [text_before, CloudName, ModulePath, content, CloudName, ModulePath, content, ...]
    for i in range(1, len(cloud_sections), 3):
        cloud_name = cloud_sections[i].strip()
        module_path = cloud_sections[i + 1].strip()
        content = cloud_sections[i + 2]

        print(f"🌩️ Processing {cloud_name} → {module_path}")

        # Match Terraform file blocks inside this cloud section
        file_pattern = r"####\s*([^\n]+\.(?:tf|tfvars|tf.json))\n```[\w]*\n(.*?)```"
        matches = re.findall(file_pattern, content, re.DOTALL)

        if not matches:
            print(f"⚠️ No Terraform files found under {cloud_name} / {module_path}")
            continue

        for filename, filecontent in matches:
            filename = filename.strip()
            filecontent = filecontent.strip() + "\n"

            # Full path (terraform/modules/aws/main.tf, etc.)
            filepath = os.path.join(TERRAFORM_DIR, module_path, filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)

            with open(filepath, "w") as f:
                f.write(filecontent)

            print(f"✅ Saved {filepath}")

    return f"🎉 Multi-cloud Terraform files generated inside {TERRAFORM_DIR}/"


def _single_cloud_parser(response, TERRAFORM_DIR):
    """Fallback parser if no cloud sections exist"""
    pattern = r"([^\n:]+\.(?:tf|tfvars|tf.json))\n(.*?)(?=(?:\n\S+\.(?:tf|tfvars|tf.json))|$)"
    matches = re.findall(pattern, response, re.DOTALL)

    if not matches:
        print("❌ Parsing failed — no files detected.")
        return "❌ Parsing failed — no files detected."

    for filename, content in matches:
        filename = filename.strip().rstrip(":")
        content = content.strip() + "\n"

        filepath = os.path.join(TERRAFORM_DIR, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, "w") as f:
            f.write(content)

        print(f"✅ Saved {filepath}")

    return "🎉 All Terraform files generated in single cloud mode."
