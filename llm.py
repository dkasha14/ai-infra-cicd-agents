import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class LLMClient:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not set")

        self.client = Groq(api_key=api_key)

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0.1,
            messages=[
                {
                    "role": "system",
                    "content": "You are a strict DevOps code generator. Follow format exactly."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return response.choices[0].message.content.strip()


class IaCAgent:
    def __init__(self):
        self.llm = LLMClient()

    # ============================================================
    # Terraform Generation
    # ============================================================
    def generate_terraform(self, user_input: str, mode: str = "Standard", cloud: str = "AWS") -> str:

        if cloud == "Azure":
            provider_block = "azurerm"
            provider_rules = """
- Use azurerm provider
- Include resource group
- Use Azure naming conventions
- ONLY generate resources explicitly mentioned in the requirement
- DO NOT add any additional resources unless explicitly requested
- Do not assume best practices that introduce new services
- DO NOT use deprecated resource "azurerm_virtual_machine"
- Use azurerm_linux_virtual_machine or azurerm_windows_virtual_machine
- Do NOT rely on Azure CLI authentication
- Always configure provider using environment variables (ARM_*)
- Provider block must only include:
  provider "azurerm" {
    features {}
  }

- Must include:
  os_disk
  source_image_reference
  admin_username
  network_interface_ids

- Resource group and network interface must exist
"""
        else:
            provider_block = "aws"
            provider_rules = """
- Use AWS provider
- Use AWS resources only
"""

        if mode == "Modular":
            prompt = f"""
Generate Terraform code using MODULES for {cloud}.

STRICT OUTPUT FORMAT:

main.tf
<code>

modules/network/main.tf
<code>

modules/compute/main.tf
<code>

modules/storage/main.tf
<code>

Rules:
- No markdown
- No explanations
- Use provider "{provider_block}"
{provider_rules}
- Every module input variable MUST be defined inside that module
- Outputs from one module can be passed to another module
- NEVER reference a module inside itself
- Avoid reserved names: version, source, providers, count, for_each
- ONLY generate resources explicitly mentioned in the requirement
- DO NOT add any additional resources (e.g., S3, RDS, IAM) unless explicitly requested
- Do not assume best practices that introduce new services
- Code must be valid

Requirement:
{user_input}
"""
        else:
            prompt = f"""
Generate Terraform code for {cloud}.

STRICT OUTPUT FORMAT:

main.tf
<code>

variables.tf
<code>

outputs.tf
<code>

Rules:
- No markdown
- No explanations
- Use provider "{provider_block}"
{provider_rules}
- Avoid reserved names: version, source, providers, count, for_each
- Code must be valid

Requirement:
{user_input}
"""

        return self.llm.generate(prompt)

    # ============================================================
    # Jenkins Pipeline Generation (FIXED LOCATION)
    # ============================================================
    def generate_pipeline(self, context: str, app_type: str = "java", pipeline_type: str = "Build") -> str:

        if app_type == "java":
            build_cmd = "mvn clean package"
        elif app_type == ".net":
            build_cmd = "dotnet build --configuration Release"
        elif app_type == "nodejs":
            build_cmd = "npm install && npm run build"
        else:
            build_cmd = "echo Build step"

        prompt = f"""
Generate a Jenkins pipeline.

STRICT RULES:
- Output only Jenkinsfile
- No markdown
- No explanation

Stages must include:
- Checkout
- Build (use: {build_cmd})
- Terraform Init
- Terraform Plan

Pipeline Type:
{pipeline_type}

Context:
{context}
"""

        return self.llm.generate(prompt)