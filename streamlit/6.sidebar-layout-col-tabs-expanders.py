# app.py — Step 6
import streamlit as st

st.set_page_config(page_title="Step 7", page_icon="📐", layout="wide")
st.title("Step 6: Layout Patterns")

with st.sidebar:
    st.header("Filters")
    project = st.text_input("Project", "platform-x")
    region = st.selectbox("Region", ["us-east-1", "eu-west-1", "me-central-1"])

kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Builds", 120, "+12")
kpi2.metric("Failures", 3, "-1")
kpi3.metric("Coverage", "91.2%", "+0.4%")

tab_data, tab_settings = st.tabs(["Data", "Advanced settings"])
with tab_data:
    st.write(f"Current filters: **{project} / {region}**")
with tab_settings:
    with st.expander("Tuning"):
        st.slider("Threshold", 0, 100, 60)
        st.text_input("Notes")
