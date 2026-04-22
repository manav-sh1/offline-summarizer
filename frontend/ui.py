from __future__ import annotations

import streamlit as st
import requests

from frontend.api_client import TextForgeApiClient
from frontend.components import render_header, render_sidebar, render_result_card
from logging_config import get_logger

logger = get_logger(__name__)

@st.cache_resource
def get_api_client() -> TextForgeApiClient:
    return TextForgeApiClient()

def main() -> None:
    # 1. Page Configuration and Theming
    st.set_page_config(
        page_title="TextForge | AI Document Analysis", 
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for premium feel
    st.markdown("""
        <style>
            .stTextArea textarea { font-family: 'Inter', sans-serif; font-size: 1.1rem; }
            .stTabs [data-baseweb="tab-list"] { gap: 10px; }
            .stTabs [data-baseweb="tab"] { 
                background-color: #f1f3f5; 
                padding: 12px 24px; 
                border-radius: 8px 8px 0 0; 
                border: 1px solid #dee2e6;
                color: #495057 !important;
            }
            .stTabs [aria-selected="true"] { 
                background-color: #ffffff !important; 
                border-bottom: 3px solid #0083B8 !important; 
                font-weight: 600;
                color: #0083B8 !important;
            }
            .main { background-color: #ffffff; }
        </style>
    """, unsafe_allow_html=True)

    # 2. Sidebar Settings
    length, top_k, query = render_sidebar()
    
    render_header()
    client = get_api_client()
    
    # Subtle health check
    try:
        client.health()
    except requests.RequestException:
        st.error("Backend Offline: Ensure the FastAPI server is running for analysis.")

    # 3. Session State Initialization
    if "input_text" not in st.session_state:
        st.session_state.input_text = ""
    if "analysis_result" not in st.session_state:
        st.session_state.analysis_result = None

    # 4. Main Interaction Area
    tab_manual, tab_upload = st.tabs(["Manual Text", "Document Upload"])

    with tab_manual:
        text = st.text_area(
            "Input text for analysis", 
            value=st.session_state.input_text,
            placeholder="Paste your text here (min 20 characters)...",
            key="text_area_main",
            label_visibility="collapsed"
        )
        st.session_state.input_text = text

    with tab_upload:
        uploaded_file = st.file_uploader(
            "Upload a document (PDF / DOCX)", 
            type=["pdf", "docx"],
            help="Extract text from docs up to 50 pages.",
            label_visibility="collapsed"
        )
        if uploaded_file:
            st.info(f"Selected: {uploaded_file.name}")
            col_extract, col_summ = st.columns(2)
            file_bytes = uploaded_file.getvalue()
            
            with col_extract:
                if st.button("Load into Editor", use_container_width=True):
                    try:
                        with st.spinner("Extracting content..."):
                            response = client.parse(file_bytes, uploaded_file.name)
                            st.session_state.input_text = response["text"]
                            st.success("Extracted! Switch to the 'Manual Text' tab to edit.")
                            st.rerun()
                    except Exception as e:
                        st.error(f"Extraction failed: {e}")
            
            with col_summ:
                if st.button("Summarize Directly", use_container_width=True):
                    try:
                        with st.spinner("Analyzing document..."):
                            response = client.summarize_file(file_bytes, uploaded_file.name, length, query or None)
                            st.session_state.analysis_result = {
                                "type": "Summary",
                                "title": f"Summary: {uploaded_file.name}",
                                "body": response["summary"],
                                "provider": response["provider"]
                            }
                    except Exception as e:
                        st.error(f"Analysis failed: {e}")

    # 5. Core Actions (Action Bar)
    st.divider()
    act_col1, act_col2, act_col3 = st.columns(3)
    
    with act_col1:
        if st.button("Summarize Text", use_container_width=True, type="primary"):
            _run_analysis(client.summarize, "Summary", "Summary Report", text=st.session_state.input_text, length=length, query=query or None)
            
    with act_col2:
        if st.button("Extract Keywords", use_container_width=True):
            _run_analysis(client.keywords, "Keywords", "Extracted Keywords", text=st.session_state.input_text, top_k=top_k)
            
    with act_col3:
        if st.button("Fix Grammar", use_container_width=True):
            _run_analysis(client.grammar, "Grammar", "Grammar Refinement", text=st.session_state.input_text)

    # 6. Result Rendering (Single Sticky Location)
    if st.session_state.analysis_result:
        st.divider()
        result = st.session_state.analysis_result
        
        if result["type"] == "Grammar":
            _render_grammar_result(result)
        elif result["type"] == "Keywords":
             keywords = result["body"]
             content = ", ".join(keywords) if isinstance(keywords, list) else str(keywords)
             render_result_card(result["title"], content, result.get("provider"))
        else:
            render_result_card(result["title"], result["body"], result.get("provider"))

def _run_analysis(method, res_type, title, **kwargs):
    text = kwargs.get("text", "")
    if not text or len(text.strip()) < 20:
        st.warning("Please provide at least 20 characters of text for analysis.")
        return

    try:
        with st.spinner(f"Processing {res_type.lower()}..."):
            response = method(**kwargs)
            
            if res_type == "Summary":
                body = response["summary"]
            elif res_type == "Keywords":
                body = response["keywords"]
            elif res_type == "Grammar":
                body = {
                    "corrected": response["corrected_text"],
                    "issues": response["issues"]
                }
            
            st.session_state.analysis_result = {
                "type": res_type,
                "title": title,
                "body": body,
                "provider": response.get("provider", "Local Engine")
            }
    except Exception as e:
        logger.error(f"{res_type} analysis failed: {e}")
        st.error(f"Analysis failed: {str(e)}")

def _render_grammar_result(result):
    with st.container(border=True):
        st.markdown(f"### {result['title']}")
        st.markdown("#### Corrected Version:")
        st.success(result["body"]["corrected"])
        
        if result["body"]["issues"]:
            with st.expander("View suggested changes"):
                for issue in result["body"]["issues"]:
                    st.markdown(f"**{issue['message']}**")
                    st.caption(f"Context: `{issue['context']}` | Suggested: {', '.join(issue['replacements']) or 'Check syntax'}")
        
        st.caption(f"Provider: {result['provider']}")

if __name__ == "__main__":
    main()
