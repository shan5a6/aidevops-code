import streamlit as st
import subprocess
import os
import re

from agent import terraform , llm, format, dataparsing 

# Page Config
st.set_page_config(page_title="Terraform Agent", layout="centered")
st.title("🌍 Terraform Agent")

from dotenv import load_dotenv
load_dotenv()

# ========== User Prompt ==========
user_prompt = st.text_area("Enter your prompt:", placeholder="Type your Terraform request here...")

# ========== Generate Terraform Code ==========
if st.button("Generate Terraform code"):
    st.subheader("Generated Terraform Code")
    # Calling LLM to fetch data 
    response = llm.calling_groq(user_prompt)
    # Printing collected data on screen 
    st.code(response, language="hcl")
    # Parsing data to multiple files 
    dataparsing.contentparsing(response)

# ========== Terraform Operations ==========
st.subheader("Terraform Operations")

# --- Values file selection ---
terraform_dir = os.path.join(os.getcwd(), "terraform")
available_tfvars = [f for f in os.listdir(terraform_dir) if f.endswith(".tfvars")] if os.path.exists(terraform_dir) else []
selected_tfvars = st.multiselect("Select values file(s):", available_tfvars)

col1, col2, col3, col4, col5, col6 = st.columns(6)

# Keep track of which action is clicked
action = None

with col1:
    if st.button("Terraform Plan"):
        action = "plan"

with col2:
    if st.button("Terraform Apply"):
        action = "apply"

with col3:
    if st.button("Terraform Destroy"):
        action = "destroy"

with col4:
    if st.button("Terraform Validate"):
        action = "validate"

with col5:
    if st.button("Terraform Format"):
        action = "format"

with col6:
    if st.button("Terraform Explain"):
        action = "explain"

# --- Show output full width ---
if action:
    if action in ["plan", "apply", "destroy"]:
        result = terraform.run_terraform_command(action, values_files=selected_tfvars)
        st.subheader(f"{action.capitalize()} Output")
        st.code(format.clean_output(result), language="bash")

    elif action == "validate":
        result = terraform.terraform_validate()
        st.subheader("Validate Output")
        st.code(format.clean_output(result), language="bash")

    elif action == "format":
        result = terraform.terraform_format()
        st.subheader("Format Output")
        st.code(format.clean_output(result), language="bash")

    elif action == "explain":
        result = terraform.terraform_explain()
        st.subheader("Code Explanation")
        st.code(format.clean_output(result), language="bash")

# ========== Show User Inputs ==========
if user_prompt:
    st.subheader("📌 Captured Inputs")
    st.write("**User Prompt:**", user_prompt)


# --- Enhanced code with cicd 
# === Jenkins Pipeline UI ===
st.subheader("🛠️ Jenkins Pipeline Generator")

pipeline_type = st.selectbox(
    "Choose pipeline type",
    ["jenkins-pr-pipeline", "jenkins-build-pipeline"]
)

jenkins_prompt = st.text_area(
    "Enter pipeline requirements:",
    placeholder="Example: checkout repo, run terraform fmt, terraform plan, build docker image, run unit tests..."
)

if st.button("Generate Jenkinsfile with Groq"):
    if not jenkins_prompt.strip():
        st.warning("⚠️ Please enter pipeline requirements before generating.")
    else:
        with st.spinner("Calling Groq to generate Jenkinsfile..."):
            try:
                messages = [
                    {"role": "system", "content": "You are a CI/CD assistant that writes production-ready Jenkins pipelines."},
                    {"role": "user", "content": f"Generate a {pipeline_type} Jenkinsfile with the following requirements:\n{jenkins_prompt}"}
                ]

                jenkins_code = llm.calling_groq(messages)

                # store in session so it persists after rerun
                st.session_state["jenkins_code"] = jenkins_code

            except Exception as e:
                st.error(f"❌ Groq API call failed: {e}")

# Show editable Jenkinsfile if code exists
if "jenkins_code" in st.session_state:
    st.subheader("📜 Generated Jenkinsfile (editable)")

    # Editable text area so user can tweak before saving
    updated_code = st.text_area(
        "Review & Edit Jenkinsfile:",
        st.session_state["jenkins_code"],
        height=400
    )

    if st.button("✅ Save Jenkinsfile"):
        save_dir = "jenkins"
        os.makedirs(save_dir, exist_ok=True)

        # Save directly as "jenkins-pr-pipeline" or "jenkins-build-pipeline"
        filepath = os.path.join(save_dir, pipeline_type)

        with open(filepath, "w") as f:
            f.write(updated_code)

        # update session state with latest edits
        st.session_state["jenkins_code"] = updated_code

        st.success(f"🎉 Jenkinsfile saved to {filepath}")
