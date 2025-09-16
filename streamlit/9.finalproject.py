import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Streamlit Demo App", layout="wide")

st.title("📊 Simple Streamlit Demo App")
st.write("This app demonstrates core Streamlit widgets in a simple, effective way.")

# Sidebar Navigation
page = st.sidebar.radio("Choose a page", ["Home", "Form", "Data", "Chart"])

if page == "Home":
    st.header("Welcome")
    st.write("Use the sidebar to explore different pages and features.")

elif page == "Form":
    st.header("Interactive Form")
    with st.form("user_form"):
        name = st.text_input("Your Name")
        age = st.number_input("Your Age", min_value=1, max_value=120, value=25)
        role = st.radio("Role", ["Developer", "Tester", "Manager"])
        env = st.selectbox("Environment", ["dev", "staging", "prod"])
        rating = st.slider("Satisfaction (0-10)", 0, 10, 5)
        submitted = st.form_submit_button("Submit")
    
    if submitted:
        st.success(f"Hello {name}, you are {age} years old, a {role}, working in {env} with rating {rating}.")

elif page == "Data":
    st.header("DataFrame & File Upload")
    uploaded_file = st.file_uploader("Upload CSV", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df)
    else:
        st.info("Upload a CSV to see the preview.")

elif page == "Chart":
    st.header("Quick Chart")
    st.write("Generating sample data:")
    data = pd.DataFrame({
        "x": np.arange(0, 50),
        "y": np.random.randn(50).cumsum()
    })
    st.line_chart(data, x="x", y="y")

st.markdown("---")
st.caption("Simple Streamlit Demo — Designed for Training")
