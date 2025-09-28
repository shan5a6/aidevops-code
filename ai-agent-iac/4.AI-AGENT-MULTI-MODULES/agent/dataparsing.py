def contentparsing(response):
    import re, os, shutil

    # Optional: Clean existing terraform dir before writing new files
    TERRAFORM_DIR = os.path.join(os.getcwd(), "terraform")
    if os.path.exists(TERRAFORM_DIR):
        shutil.rmtree(TERRAFORM_DIR)
    os.makedirs(TERRAFORM_DIR, exist_ok=True)

    # ✅ Match only valid Terraform filenames
    pattern = r"([^\n:]+\.(?:tf|tfvars|tf.json))\n(.*?)(?=(?:\n\S+\.(?:tf|tfvars|tf.json))|$)"
    matches = re.findall(pattern, response, re.DOTALL)

    if not matches:
        print("⚠️ No valid Terraform file blocks found. Check LLM response format.")
        return "❌ Parsing failed — no files detected."

    for filename, content in matches:
        filename = filename.strip().rstrip(":")
        content = content.strip() + "\n"

        # Full path inside ./terraform
        filepath = os.path.join(TERRAFORM_DIR, filename)

        # ✅ Ensure parent dirs exist (modules/vpc, modules/ec2, etc.)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # Write content
        with open(filepath, "w") as f:
            f.write(content)

        print(f"✅ Saved {filepath}")

    return "🎉 All Terraform files & modules generated inside ./terraform/"
