import streamlit as st
import requests

# --- Page Config ---
st.set_page_config(page_title="AI Planet PDF Q&A", layout="wide", initial_sidebar_state="collapsed")

# --- Session State Init ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "doc_id" not in st.session_state:
    st.session_state.doc_id = None
if "filename" not in st.session_state:
    st.session_state.filename = None

# --- Custom CSS ---
st.markdown("""
    <style>
        html, body, [data-testid="stApp"] {
            height: 100%;
            overflow: auto;
            margin: 0;
        }

        .top-bar {
            background-color: #F8F9FA;
            height: 70px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 2rem;
            border-bottom: 1px solid #e1e1e1;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 1000;
        }

        .chat-scroll-area {
            position: absolute;
            top: 70px;
            bottom: 90px;
            left: 0;
            right: 0;
            overflow-y: auto;
            padding: 1rem 2rem;
        }

        .message {
            border-radius: 12px;
            padding: 1rem;
            margin: 0.5rem 0;
            max-width: 80%;
            display: flex;
            align-items: center;
        }

        .user-msg {
            background-color: #DBEAFE;
            margin-left: auto;
            text-align: right;
            flex-direction: row-reverse;
        }

        .bot-msg {
            background-color: #F3F4F6;
            margin-right: auto;
        }

        .icon {
            width: 32px;
            height: 32px;
            margin: 0 0.5rem;
        }

        .input-bar {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            padding: 1rem 2rem;
            background-color: white;
            border-top: 1px solid #e1e1e1;
            display: flex;
            gap: 10px;
            z-index: 1000;
            animation: slideUp 0.4s ease-out;
        }

        .stTextInput > div > div > input {
            border-radius: 10px;
            padding: 0.6rem;
        }

        .stButton > button {
            border-radius: 10px;
            background-color: #4F46E5;
            color: white;
            padding: 0.5rem 1rem;
        }

        @keyframes slideUp {
            from {
                transform: translateY(100%);
                opacity: 0;
            }
            to {
                transform: translateY(0%);
                opacity: 1;
            }
        }
    </style>
""", unsafe_allow_html=True)

# --- Top Bar ---
st.markdown('<div class="top-bar">', unsafe_allow_html=True)
col1, col2 = st.columns([6, 1])
with col1:
    st.image("AI_Planet-logo-removebg-preview.png", width=120)
with col2:
    if st.session_state.filename:
        st.markdown(f"**📄 {st.session_state.filename}**")
    else:
        uploaded_file = st.file_uploader("", type="pdf", label_visibility="collapsed")
        if uploaded_file:
            with st.spinner("Uploading..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                    response = requests.post("http://localhost:8000/upload", files=files)
                    result = response.json()
                    if response.status_code == 200 and result.get("document_id"):
                        st.session_state.doc_id = result["document_id"]
                        st.session_state.filename = uploaded_file.name
                        st.success("✅ Upload successful!")
                        st.rerun()
                    else:
                        st.error(result.get("error", "Upload failed."))
                except Exception as e:
                    st.error(f"Exception: {str(e)}")
st.markdown('</div>', unsafe_allow_html=True)

# --- Chat Section ---
st.markdown('<div class="chat-scroll-area">', unsafe_allow_html=True)
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"""
            <div class="message user-msg">
                <img src="https://cdn-icons-png.flaticon.com/512/149/149071.png" class="icon"/>
                {msg["content"]}
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="message bot-msg">
                <img src="https://cdn-icons-png.flaticon.com/512/4712/4712103.png" class="icon"/>
                {msg["content"]}
            </div>
        """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- Input Bar (Light with Animation) ---
st.markdown('<div class="input-bar">', unsafe_allow_html=True)
input_col1, input_col2 = st.columns([6, 1])
with input_col1:
    question = st.text_input("Ask your question:", label_visibility="collapsed", key="input_question",
                             placeholder="Type your question here...", disabled=not st.session_state.doc_id)
with input_col2:
    send_clicked = st.button("Send", disabled=not st.session_state.doc_id)
st.markdown('</div>', unsafe_allow_html=True)

# --- Send Logic ---
if send_clicked and question.strip():
    st.session_state.chat_history.append({"role": "user", "content": question})
    with st.spinner("Generating..."):
        try: 
            response = requests.post(
                "http://localhost:8000/ask",
                json={"document_id": st.session_state.doc_id, "question": question}
            )
            result = response.json()
            answer = result.get("answer", result.get("error", "No answer returned."))
        except Exception as e:
            answer = f"Exception occurred: {str(e)}"
    st.session_state.chat_history.append({"role": "bot", "content": answer})
    st.rerun()
