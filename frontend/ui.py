from __future__ import annotations

import requests
import streamlit as st

from frontend.api_client import TextForgeApiClient
from frontend.components import render_header, render_result, render_sidebar
from logging_config import get_logger


logger = get_logger(__name__)


def main() -> None:
    logger.info("Rendering Streamlit UI")
    st.set_page_config(page_title="TextForge", layout="wide")
    render_sidebar()
    render_header()

    client = TextForgeApiClient()
    _render_health_banner(client)

    text = st.text_area("Input text", height=280, placeholder="Paste the text you want to process...")
    col1, col2 = st.columns(2)
    with col1:
        length = st.selectbox("Summary length", options=["short", "medium", "long"], index=1)
    with col2:
        top_k = st.slider("Keyword count", min_value=3, max_value=10, value=8)
    query = st.text_input("Focus query", placeholder="Optional: e.g. benefits of AI")

    action_col1, action_col2, action_col3 = st.columns(3)
    with action_col1:
        summarize_clicked = st.button("Summarize", use_container_width=True)
    with action_col2:
        keywords_clicked = st.button("Keywords", use_container_width=True)
    with action_col3:
        grammar_clicked = st.button("Grammar", use_container_width=True)

    if summarize_clicked:
        logger.info("Summarize button clicked")
        _require_text(text)
        try:
            response = client.summarize(text=text, length=length, query=query or None)
            render_result("Summary", response["summary"])
            st.caption(f"Provider: {response['provider']}")
        except requests.RequestException as exc:
            logger.warning("Summarize request failed: %s", exc)
            st.error(f"Unable to summarize text: {exc}")

    if keywords_clicked:
        logger.info("Keywords button clicked")
        _require_text(text)
        try:
            response = client.keywords(text=text, top_k=top_k)
            render_result("Keywords", ", ".join(response["keywords"]) or "No keywords found.")
        except requests.RequestException as exc:
            logger.warning("Keywords request failed: %s", exc)
            st.error(f"Unable to extract keywords: {exc}")

    if grammar_clicked:
        logger.info("Grammar button clicked")
        _require_text(text)
        try:
            response = client.grammar(text=text)
            if response["issues"]:
                st.subheader("Grammar Issues")
                for issue in response["issues"]:
                    st.markdown(
                        f"- **{issue['message']}**\n"
                        f"Context: `{issue['context']}`\n"
                        f"Suggestions: {', '.join(issue['replacements']) or 'No suggestions'}"
                    )
            else:
                render_result("Grammar", "No grammar issues detected.")
            st.caption(f"Provider: {response['provider']}")
        except requests.RequestException as exc:
            logger.warning("Grammar request failed: %s", exc)
            st.error(f"Unable to check grammar: {exc}")


def _render_health_banner(client: TextForgeApiClient) -> None:
    try:
        client.health()
        logger.info("Backend healthcheck succeeded from UI")
        st.success("Backend connected.")
    except requests.RequestException as exc:
        logger.warning("Backend healthcheck failed from UI: %s", exc)
        st.error("Backend unavailable. Start the FastAPI server before using the app.")


def _require_text(text: str) -> None:
    if not text or len(text.strip()) < 20:
        logger.info("Rejected input because it was shorter than 20 characters")
        st.warning("Please enter at least 20 characters of text.")
        st.stop()


main()
