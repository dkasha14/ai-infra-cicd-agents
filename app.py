import streamlit as st
from llm import IaCAgent
from dataparsing import contentparsing
from terraform import (
    run_terraform_command,
    terraform_validate,
    terraform_format,
    terraform_explain
)
from format import clean_output
import os

# ---------------------------
# Init
# ---------------------------
agent = IaCAgent()

st.set_page_config(page_title="AI IaC Agent Platform", layout="wide")

# Session state
if "tf_output" not in st.session_state:
    st.session_state.tf_output = ""

# ---------------------------
# Sidebar
# ---------------------------
st.sidebar.title("🧠 Agents")

agent_type = st.sidebar.radio(
    "Select Agent",
    ["IaC Agent", "Jenkins Agent", "GitOps Agent"]
)

cloud_provider = st.sidebar.selectbox(
    "☁️ Cloud Provider",
    ["AWS", "Azure"]
)

# ---------------------------
# Title
# ---------------------------
st.title("🌍 AI-Driven DevOps Agent Platform")

# ============================================================
# 🔷 IAC AGENT
# ============================================================
if agent_type == "IaC Agent":

    st.header("🏗️ Terraform Agent")

    iac_mode = st.radio(
        "Terraform Mode",
        ["Standard", "Modular"]
    )

    user_input = st.text_area(
        "📥 Infrastructure Prompt",
        placeholder="Create VPC, EC2, S3 with best practices"
    )

    st.info(f"Generating Terraform for: {cloud_provider}")

    if st.button("🚀 Generate Terraform Code"):
        if not user_input.strip():
            st.warning("Please enter a requirement")
        else:
            response = agent.generate_terraform(user_input, iac_mode, cloud_provider)

            try:
                msg = contentparsing(response)
                st.success(msg)
            except Exception as e:
                st.error(str(e))

            st.subheader("Generated Code")
            st.code(response, language="hcl")

    # ---------------------------
    # Terraform Operations
    # ---------------------------
    st.subheader("⚙️ Terraform Operations")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("📋 Plan"):
            with st.spinner("Running Terraform Plan..."):
                st.session_state.tf_output = clean_output(run_terraform_command("plan"))

    with col2:
        if st.button("🚀 Apply"):
            if not os.path.exists("terraform"):
                st.error("❌ Generate Terraform first")
            else:
                with st.spinner("Applying Infrastructure..."):
                    st.session_state.tf_output = clean_output(run_terraform_command("apply"))

    with col3:
        if st.button("🔥 Destroy"):
            if not os.path.exists("terraform"):
                st.error("❌ Generate Terraform first")
            else:
                with st.spinner("Destroying Infrastructure..."):
                    st.session_state.tf_output = clean_output(run_terraform_command("destroy"))

    with col4:
        if st.button("✅ Validate"):
            with st.spinner("Validating Terraform..."):
                st.session_state.tf_output = terraform_validate()

    col5, col6 = st.columns(2)

    with col5:
        if st.button("🧹 Format"):
            with st.spinner("Formatting Terraform..."):
                st.session_state.tf_output = terraform_format()

    with col6:
        if st.button("🧠 Explain"):
            with st.spinner("Explaining Terraform..."):
                st.session_state.tf_output = terraform_explain()

    # ---------------------------
    # Output
    # ---------------------------
    if st.session_state.tf_output:
        st.subheader("📄 Output")
        st.code(st.session_state.tf_output)

# ============================================================
# 🔷 JENKINS AGENT
# ============================================================
elif agent_type == "Jenkins Agent":

    st.header("🔧 Jenkins Pipeline Generator")

    github_url = st.text_input("GitHub Repository URL")
    email = st.text_input("Notification Email")
    subject = st.text_input("Email Subject", value="Terraform Pipeline Status")

    env = st.selectbox("Environment", ["dev", "sit", "prod"])

    app_type = st.selectbox(
        "Application Type",
        ["java", ".net", "nodejs"]
    )

    pipeline_type = st.selectbox(
        "Pipeline Type",
        ["PR Pipeline", "Build Pipeline", "Deployment Pipeline"]
    )

    if st.button("🚀 Generate Jenkinsfile"):

        if not github_url or not email:
            st.warning("GitHub URL and Email are required")
        else:

            # ---------------------------
            # Trigger Block
            # ---------------------------
            trigger_block = ""

            if pipeline_type == "PR Pipeline":
                trigger_block = """
    triggers {
        githubPullRequest {
            useGitHubHooks()
        }
    }
"""

            # ---------------------------
            # Build Stage (APP SPECIFIC ✅)
            # ---------------------------
            build_stage = ""

            if app_type == "java":
                build_stage = """
        stage('Build - Java') {
            steps {
                sh 'mvn clean package'
            }
        }
"""
            elif app_type == ".net":
                build_stage = """
        stage('Build - .NET') {
            steps {
                sh 'dotnet restore'
                sh 'dotnet build --configuration Release'
            }
        }
"""
            elif app_type == "nodejs":
                build_stage = """
        stage('Build - NodeJS') {
            steps {
                sh 'npm install'
                sh 'npm run build'
            }
        }
"""

            # ---------------------------
            # FINAL PIPELINE (FIXED ✅)
            # ---------------------------
            pipeline = f"""
pipeline {{
    agent any
{trigger_block}
    environment {{
        ENV = "{env}"
    }}

    stages {{

        stage('Checkout') {{
            steps {{
                git '{github_url}'
            }}
        }}

{build_stage}

        stage('Terraform Init') {{
            steps {{
                sh 'terraform init'
            }}
        }}

        stage('Terraform Validate') {{
            steps {{
                sh 'terraform validate'
            }}
        }}

        stage('Terraform Plan') {{
            steps {{
                sh 'terraform plan'
            }}
        }}
"""

            # ---------------------------
            # Deployment Only for Deploy Pipeline
            # ---------------------------
            if pipeline_type == "Deployment Pipeline":
                pipeline += f"""
        stage('Manual Approval') {{
            steps {{
                input 'Approve deployment to {env}?'
            }}
        }}

        stage('Terraform Apply') {{
            steps {{
                sh 'terraform apply -auto-approve'
            }}
        }}
"""

            pipeline += f"""
    }}

    post {{
        failure {{
            mail to: '{email}',
                 subject: '{subject} - FAILED',
                 body: 'Pipeline failed in {env} environment.'
        }}
        success {{
            mail to: '{email}',
                 subject: '{subject} - SUCCESS',
                 body: 'Pipeline succeeded in {env} environment.'
        }}
    }}
}}
"""

            st.subheader("📜 Generated Jenkinsfile")
            st.code(pipeline, language="groovy")
# ============================================================
# 🔷 GITOPS AGENT
# ============================================================
elif agent_type == "GitOps Agent":

    st.header("🔄 GitOps Agent")
    st.info("GitOps integration coming next (ArgoCD / Flux)")