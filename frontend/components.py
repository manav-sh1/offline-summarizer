import streamlit as st


def render_header() -> None:
    st.title("TextForge")
    st.caption("Offline summarization, keywords, and grammar checks with a local-first architecture.")


def render_sidebar() -> None:
    st.sidebar.title("Controls")
    st.sidebar.info("Start the FastAPI backend first, then use this UI to call the local API.")


def render_result(title: str, body: str) -> None:
    st.subheader(title)
    st.write(body)
