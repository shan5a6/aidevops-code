# app.py — Step 7
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Step 7", page_icon="🗂️", layout="wide")
st.title("Step 7: Upload CSV & Explore")

file = st.file_uploader("Upload a CSV", type=["csv"])
if not file:
    st.info("Upload a file to continue.")
    st.stop()

df = pd.read_csv(file)

st.subheader("Preview")
st.dataframe(df, use_container_width=True)

st.subheader("Quick chart")
numeric_cols = df.select_dtypes("number").columns.tolist()
if len(numeric_cols) >= 1:
    x = st.selectbox("X axis", df.columns, index=0)
    y = st.selectbox("Y axis (numeric)", numeric_cols, index=0)
    st.line_chart(df.set_index(x)[y])
else:
    st.warning("No numeric columns to plot.")
