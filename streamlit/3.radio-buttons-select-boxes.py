# app.py — Step 3
import streamlit as st

st.set_page_config(page_title="Step 3", page_icon="📻")
st.title("Step 3: Radio & Select")

env = st.radio("Choose environment", ["dev", "staging", "prod"], horizontal=True)
service = st.selectbox("Service", ["api", "worker", "db", "cache"])

st.write(f"You selected **{env}** → **{service}**")

if env == "prod":
    st.warning("Careful! Production environment.")
else:
    st.success("Safe to experiment here.")
