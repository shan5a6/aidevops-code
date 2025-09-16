# import streamlit as st 

# st.title("Welcome to AIDEVOPS")

# st.set_page_config(page_title="DEVOPSBOT",
#     page_icon="🧊",
#     layout="wide")


# app.py — Step 1
import streamlit as st

st.set_page_config(page_title="Step 1", page_icon="✅", layout="centered")

st.title("Step 1: Hello Streamlit 👋")
st.write("This page renders from a single Python script.")

st.markdown("""
- Save this file while the app is running — it auto-reloads.
- Streamlit re-runs the script **top-to-bottom** on every interaction.
""")
