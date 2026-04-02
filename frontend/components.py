import streamlit as st

def render_header() -> None:
    st.markdown("""
        <div style="text_align: center; padding-bottom: 20px;">
            <h1 style="color: #0083B8; font-size: 3rem; margin-bottom: 0;">TextForge</h1>
            <p style="color: #666; font-size: 1.2rem;">Intelligent Document Analysis & Refinement</p>
        </div>
    """, unsafe_allow_html=True)

def render_sidebar() -> None:
    with st.sidebar:
        st.title("Controls")
        st.info("Configure your analysis preferences here.")
        
        st.divider()
        st.subheader("Analysis Parameters")
        
        length = st.selectbox(
            "Summary Length",
            options=["short", "medium", "long"],
            index=1,
            help="Choose how detailed you want the summary to be."
        )
        
        top_k = st.slider(
            "Keyword Count",
            min_value=3,
            max_value=20,
            value=8,
            help="Number of key terms to extract."
        )
        
        query = st.text_input(
            "Focus Query",
            placeholder="e.g. key findings, dates...",
            help="Optional: Guide the summarizer to focus on specific topics."
        )
        
        st.divider()
        if st.button("Clear Cache & Results", use_container_width=True):
            for key in ["result", "input_text", "active_tab", "analysis_result"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
            
        return length, top_k, query

def render_result_card(title: str, content: str, provider: str | None = None) -> None:
    with st.container(border=True):
        st.markdown(f"### {title}")
        st.write(content)
        if provider:
            st.caption(f"Powered by: {provider}")
