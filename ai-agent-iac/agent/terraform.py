import subprocess
def run_terraform_command(command,TERRAFORM_DIR="terraform"):
    try:
        subprocess.run(["terraform", "init", "-input=false"], cwd=TERRAFORM_DIR, check=True, capture_output=True)

        tf_command = ["terraform", command]
        if command in ["apply", "destroy"]:
            tf_command.append("-auto-approve")

        result = subprocess.run(tf_command, cwd=TERRAFORM_DIR, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.stderr