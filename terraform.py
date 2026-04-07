import subprocess
import os
import re
from llm import IaCAgent

agent = IaCAgent()


# ---------------------------
# Helper
# ---------------------------
def check_terraform_dir(TERRAFORM_DIR):
    if not os.path.exists(TERRAFORM_DIR):
        return False, "❌ Terraform directory not found. Generate code first."
    return True, ""


# ---------------------------
# Run Terraform Command
# ---------------------------
def run_terraform_command(command, TERRAFORM_DIR="terraform", values_files=None):

    exists, msg = check_terraform_dir(TERRAFORM_DIR)
    if not exists:
        return msg

    try:
        subprocess.run(
            ["terraform", "init", "-input=false"],
            cwd=TERRAFORM_DIR,
            capture_output=True,
            text=True,
            check=True
        )

        tf_command = ["terraform", command]

        if command in ["apply", "destroy"]:
            tf_command.append("-auto-approve")

        if values_files:
            for vf in values_files:
                tf_command.extend(["-var-file", vf])

        result = subprocess.run(
            tf_command,
            cwd=TERRAFORM_DIR,
            capture_output=True,
            text=True,
            check=True
        )

        clean = re.sub(r'\x1b\[[0-9;]*m', '', result.stdout)
        return clean if clean.strip() else "✅ Command executed successfully"

    except subprocess.CalledProcessError as e:
        error_clean = re.sub(r'\x1b\[[0-9;]*m', '', e.stderr)
        return f"❌ ERROR:\n{error_clean}"


# ---------------------------
# Validate
# ---------------------------
def terraform_validate(TERRAFORM_DIR="terraform"):

    exists, msg = check_terraform_dir(TERRAFORM_DIR)
    if not exists:
        return msg

    try:
        subprocess.run(
            ["terraform", "init", "-input=false"],
            cwd=TERRAFORM_DIR,
            capture_output=True,
            text=True,
            check=True
        )

        result = subprocess.run(
            ["terraform", "validate"],
            cwd=TERRAFORM_DIR,
            capture_output=True,
            text=True,
            check=True
        )

        clean = re.sub(r'\x1b\[[0-9;]*m', '', result.stdout)
        return clean if clean.strip() else "✅ Terraform configuration is valid"

    except subprocess.CalledProcessError as e:
        error_clean = re.sub(r'\x1b\[[0-9;]*m', '', e.stderr)
        return f"❌ VALIDATION ERROR:\n{error_clean}"


# ---------------------------
# Format
# ---------------------------
def terraform_format(TERRAFORM_DIR="terraform"):

    exists, msg = check_terraform_dir(TERRAFORM_DIR)
    if not exists:
        return msg

    try:
        subprocess.run(
            ["terraform", "init", "-input=false"],
            cwd=TERRAFORM_DIR,
            capture_output=True,
            text=True,
            check=True
        )

        result = subprocess.run(
            ["terraform", "fmt", "-recursive"],
            cwd=TERRAFORM_DIR,
            capture_output=True,
            text=True,
            check=True
        )

        clean = re.sub(r'\x1b\[[0-9;]*m', '', result.stdout)

        if clean.strip():
            return f"🧹 Formatted Files:\n{clean}"
        else:
            return "✅ All Terraform files are properly formatted"

    except subprocess.CalledProcessError as e:
        error_clean = re.sub(r'\x1b\[[0-9;]*m', '', e.stderr)
        return f"❌ FORMAT ERROR:\n{error_clean}"


# ---------------------------
# Explain
# ---------------------------
def terraform_explain(TERRAFORM_DIR="terraform"):

    exists, msg = check_terraform_dir(TERRAFORM_DIR)
    if not exists:
        return msg

    main_tf = os.path.join(TERRAFORM_DIR, "main.tf")

    if not os.path.exists(main_tf):
        return "❌ main.tf not found. Generate Terraform first."

    with open(main_tf) as f:
        code = f.read()

    prompt = f"""
Explain this Terraform code clearly:

{code}
"""

    return agent.llm.generate(prompt)