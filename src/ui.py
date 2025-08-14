import streamlit as st
from src.config import TAB_NAMES


def render_intro():
    st.title("StyleShift: AI-Powered Writing Rephraser")
    st.divider()
    st.markdown("""
    Welcome to StyleShift! 
    Enter your text and let AI rephrase it for you.  
    Please note: inappropriate or offensive content will not be processed.
    """)


def render_output(rephrase_text: dict):
    inappropriate_text = rephrase_text['moderator']
    if inappropriate_text:
        st.warning(
            "Your message has been flagged for containing inappropriate language. "
            "Please review your text and edit your message before submitting.",
            icon="⚠️"
        )
        return

    tabs = st.tabs(TAB_NAMES)
    outputs = [
        rephrase_text['professional_output'],
        rephrase_text['casual_output'],
        rephrase_text['polite_output'],
        rephrase_text['social_media_output']
    ]

    for tab, content in zip(tabs, outputs):
        with tab:
            container = st.container(border=True)
            container.write(content)
