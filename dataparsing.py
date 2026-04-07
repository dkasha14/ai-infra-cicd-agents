def contentparsing(response: str) -> str:
    import re
    import os
    import shutil

    TERRAFORM_DIR = os.path.join(os.getcwd(), "terraform")

    # ---------------------------
    # Step 1: Reset workspace safely
    # ---------------------------
    if os.path.exists(TERRAFORM_DIR):
        shutil.rmtree(TERRAFORM_DIR)

    os.makedirs(TERRAFORM_DIR, exist_ok=True)

    # ---------------------------
    # Step 2: Extract Terraform files
    # ---------------------------
    pattern = r"([^\n:]+\.(?:tf|tfvars|tf.json))\n(.*?)(?=(?:\n\S+\.(?:tf|tfvars|tf.json))|$)"
    matches = re.findall(pattern, response, re.DOTALL)

    if not matches:
        raise ValueError("❌ Invalid LLM output: No Terraform files detected.")

    # ---------------------------
    # Step 3: Reserved keyword protection
    # ---------------------------
    RESERVED_VARIABLES = {
        "version": "app_version",
        "source": "module_source",
        "providers": "provider_config",
        "count": "resource_count",
        "for_each": "for_each_map"
    }

    # ---------------------------
    # Step 4: Write files safely
    # ---------------------------
    for filename, content in matches:

        filename = filename.strip().rstrip(":")

        # Prevent path traversal (security)
        if ".." in filename:
            raise ValueError(f"❌ Invalid file path detected: {filename}")

        filepath = os.path.join(TERRAFORM_DIR, filename)

        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # ---------------------------
        # Step 5: Sanitize variables safely
        # ---------------------------
        for bad, good in RESERVED_VARIABLES.items():
            pattern_var = f'variable "{bad}"'
            if pattern_var in content:
                content = content.replace(pattern_var, f'variable "{good}"')

        # ---------------------------
        # Step 6: Write file
        # ---------------------------
        with open(filepath, "w") as f:
            f.write(content.strip() + "\n")

    return "✅ Terraform files generated successfully"