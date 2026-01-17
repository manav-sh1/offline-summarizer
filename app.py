import streamlit as st
import time

# -------------------- Page Config --------------------
st.set_page_config(
    page_title="Offline Summarization Tool",
    layout="wide"
)

# -------------------- Session State Init --------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "user",
            "content": "Can you summarize this paragraph for me?"
        },
        {
            "role": "assistant",
            "content": "Sure! Please paste the text you want me to summarize."
        },
        {
            "role": "user",
            "content": "Artificial Intelligence is transforming industries by automating tasks, improving decision-making, and enabling new products and services."
        },
        {
            "role": "assistant",
            "content": "📝 **Summary:**\n\nArtificial Intelligence is changing industries by automating work, enhancing decisions, and creating innovative products and services."
        }
    ]

if "show_welcome" not in st.session_state:
    st.session_state.show_welcome = False  # hide welcome because demo chats exist

# -------------------- Sidebar --------------------
with st.sidebar:
    st.markdown("## ⚙️ Controls")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.show_welcome = True
        st.rerun()

    st.markdown("---")
    st.markdown(
        """
        **Offline Summarization Tool**  
        🔹 Fast  
        🔹 Private  
        🔹 Works without internet
        """
    )

# -------------------- Header --------------------
st.markdown(
    """
    <h2 style='margin-bottom:5px;'>🤖 Offline Summarization Tool</h2>
    <p style='color:gray;margin-top:0;'>Summarize text & ask questions offline</p>
    """,
    unsafe_allow_html=True
)
st.divider()

# -------------------- Welcome Screen --------------------
if st.session_state.show_welcome and not st.session_state.messages:
    st.markdown(
        """
        <div style="
            text-align:center;
            margin-top:120px;
            color:#333;
        ">
            <h1>What can I help with?</h1>
            <p style="font-size:18px;color:gray;">
                Paste text or ask a question to get started
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# -------------------- Chat Messages --------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------- Chat Input --------------------
user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state.show_welcome = False

    # Store user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Bot typing effect
    with st.chat_message("assistant"):
        placeholder = st.empty()
        temp_text = "🔍 Analyzing your input..."
        typed = ""

        for char in temp_text:
            typed += char
            placeholder.markdown(typed)
            time.sleep(0.03)

    # Demo bot logic (replace later)
    bot_reply = f"✅ **Demo Response:**\n\nYour input was received successfully.\n\n```\n{user_input}\n```"

    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_reply
    })

    st.rerun()
