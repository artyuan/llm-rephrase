import streamlit as st
from src.ui import render_intro, render_output
from src.processing import rephrase_text

render_intro()

text = st.text_input("Text")
if st.button("Process"):
    with st.spinner("Rephrasing...", show_time=True):
        if text.strip():
            result = rephrase_text(text)
            render_output(result)
        else:
            st.warning("Please enter some text before processing.", icon="⚠️")
