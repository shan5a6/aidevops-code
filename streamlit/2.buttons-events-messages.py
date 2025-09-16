# app.py — Step 2

import streamlit as st 
import time
st.set_page_config("AIDEVOPS", page_icon="🔘")
st.title("Working with buttons")

if st.button("Click for snow flow"):
    st.snow()

elif st.button("Click for baloons",type="primary"):
    st.balloons()
elif st.button("Click for progress bar"):
    progress = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.01)
        progress.progress(percent_complete + 1)
    time.sleep(1)
    st.empty()
    st.button("Rerun")