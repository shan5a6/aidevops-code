import streamlit as st
import subprocess
import os

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
    if action == "plan":
        result = terraform.run_terraform_command("plan")
        st.subheader("Plan Output")
        st.code(format.clean_output(result), language="bash")

    elif action == "apply":
        result = terraform.run_terraform_command("apply")
        st.subheader("Apply Output")
        st.code(format.clean_output(result), language="bash")

    elif action == "destroy":
        result = terraform.run_terraform_command("destroy")
        st.subheader("Destroy Output")
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
