# app.py — Step 5
import streamlit as st

st.set_page_config(page_title="Step 5", page_icon="🧾")
st.title("Step 5: Forms & Validation")

with st.form("signup"):
    email = st.text_input("Work email")
    region = st.selectbox("Region", ["us-east-1", "eu-west-1", "me-central-1"])
    accept = st.checkbox("I accept the policy")
    submitted = st.form_submit_button("Create account")

if submitted:
    if not email or "@" not in email:
        st.error("Please enter a valid email.")
    elif not accept:
        st.warning("Please accept the policy.")
    else:
        st.success(f"Account created for {email} in {region}.")
