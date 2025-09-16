# app.py — Step 4
import streamlit as st

st.set_page_config(page_title="Step 4", page_icon="⌨️")
st.title("Step 4: Inputs → Output")

name = st.text_input("Your name", placeholder="e.g., Shaan")
years = st.number_input("Years of experience", 0, 50, 10)
confidence = st.slider("Confidence to learn Streamlit", 0, 100, 70)

if st.button("Generate Intro"):
    intro = f"Hi, I'm {name or 'Anonymous'} with {years} years; confidence {confidence}%."
    st.success(intro)
