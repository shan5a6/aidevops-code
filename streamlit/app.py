import streamlit as st

# --- Page Config ---
st.set_page_config(page_title="Service Selector", page_icon="⚙️", layout="centered")

st.title("⚙️ Service & Environment Selector")

# --- Step 1: Service Selection ---
services = ["API", "Worker", "DB", "Cache"]
selected_services = st.multiselect(
    "Select the services you want to work with:",
    options=services,
    default=[],
    help="Choose one or more services"
)

# --- Step 2: Environment Dropdown ---
environments = ["dev", "staging", "prod"]
selected_environment = st.selectbox(
    "Select Environment:",
    options=environments,
    index=0,
    help="Pick the environment to deploy or run against"
)

# --- Display Results ---
st.subheader("Your Selection")
if selected_services:
    st.write(f"🔧 **Services Selected:** {', '.join(selected_services)}")
else:
    st.warning("No services selected yet.")

st.write(f"🌍 **Environment:** `{selected_environment}`")
