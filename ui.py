import streamlit as st
import time

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Offline Summarization Tool",
    layout="wide"
)

# -------------------- SESSION STATE --------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------- CSS --------------------
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

.stApp {
    background: radial-gradient(circle at top, #111827, #020617);
}

.hero {
    text-align: center;
    font-size: 46px;
    font-weight: 800;
    background: linear-gradient(90deg, #22d3ee, #6366f1, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-top: 60px;
}

.sub {
    text-align: center;
    color: #9ca3af;
    font-size: 18px;
    margin-bottom: 40px;
}

.user-msg {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    padding: 14px;
    border-radius: 14px;
    color: white;
    max-width: 70%;
    margin-left: auto;
    margin-bottom: 14px;
}

.bot-msg {
    background: #020617;
    padding: 14px;
    border-radius: 14px;
    color: #e5e7eb;
    max-width: 70%;
    margin-bottom: 14px;
    border: 1px solid #1f2937;
}

.input-box {
    margin-top: 20px;
    padding-bottom: 30px;
}
</style>
""", unsafe_allow_html=True)

# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.markdown("## ⚙ Controls")

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    mode = st.radio(
        "📄 Summary Style",
        ["Short", "Detailed", "Bullet Points", "Exam Ready"]
    )

# -------------------- HEADER --------------------
st.markdown('<div class="hero">Offline Summarization Tool</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">Fast • Private • No Internet Required</div>', unsafe_allow_html=True)

# -------------------- CHAT AREA --------------------
if not st.session_state.messages:
    st.markdown("""
    <div style="text-align:center; margin-top:120px; color:#6b7280;">
        <h2>👋 Ready when you are</h2>
        <p>Type what you want to summarize</p>
    </div>
    """, unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-msg">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-msg">{msg["content"]}</div>', unsafe_allow_html=True)

# -------------------- FORM INPUT (🔥 SAFE) --------------------
st.markdown('<div class="input-box">', unsafe_allow_html=True)

with st.form("chat_form", clear_on_submit=True):
    user_text = st.text_input(
        "",
        placeholder="Ask anything... summarize, explain, simplify",
        label_visibility="collapsed"
    )
    submitted = st.form_submit_button("Send")

st.markdown('</div>', unsafe_allow_html=True)

# -------------------- DEMO LOGIC --------------------
def demo_response(text):
    t = text.lower()

    if "summarize my large paragraph" in t or "summarise my large paragraph" in t:
        return "Sure 😄 papa, aap apna paragraph de do — main usko **short summary** me convert kar dunga."

    if len(text) > 200:
        return f"""**Summary Style:** {mode}

• Main idea extracted  
• Extra details removed  
• Simple & exam-friendly summary  

_(Demo output)_"""

    return "Please apna paragraph ya content paste karein 🙂"

# -------------------- PROCESS SUBMIT --------------------
if submitted and user_text.strip():
    st.session_state.messages.append({
        "role": "user",
        "content": user_text
    })

    with st.spinner("Thinking..."):
        time.sleep(1)

    reply = demo_response(user_text)

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })

    st.rerun()
