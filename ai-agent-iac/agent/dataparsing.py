def contentparsing(response):
    import re , os
    matches = re.findall(r"\*\*(.+?)\*\*\n(.*?)(?=\n\*\*|$)", response, re.DOTALL)

    ### 4. Create folder and store data to individual files
    TERRAFORM_DIR = os.path.join(os.getcwd(), "terraform")
    os.makedirs(TERRAFORM_DIR, exist_ok=True)

    for filename, content in matches:
        filepath = os.path.join(TERRAFORM_DIR, filename.strip())
        with open(filepath, "w") as f:
            f.write(content.strip() + "\n")
        print(f"Saved {filepath}")

    return("✅ All Terraform files generated inside ./terraform/")