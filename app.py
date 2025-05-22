import streamlit as st
import requests
from PIL import Image

# --- Page Config ---
st.set_page_config(page_title="AI Planet PDF Q&A", layout="centered")

# --- Logo and Title ---
col1, col2 = st.columns([1, 8])
with col1:
    st.image("AI_Planet-logo-removebg-preview.png", width=60)  # AI Planet logo
with col2:
    st.markdown("## AI Planet PDF Q&A Assistant")

# --- Custom CSS ---
st.markdown("""
    <style>
        .stButton > button {
            background-color: #4F46E5;
            color: white;
            padding: 0.6rem 1.2rem;
            border-radius: 10px;
            font-weight: 500;
        }
        .stTextInput > div > div > input {
            border-radius: 10px;
            padding: 0.6rem;
        }
        .message {
            border-radius: 10px;
            padding: 1rem;
            margin: 0.5rem 0;
        }
        .user-msg {
            background-color: #E0E7FF;
            text-align: right;
        }
        .bot-msg {
            background-color: #F3F4F6;
        }
    </style>
""", unsafe_allow_html=True)

# --- Session State Init ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "doc_id" not in st.session_state:
    st.session_state.doc_id = None

# --- Upload Section ---
with st.container():
    st.markdown("### 📤 Upload a PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", label_visibility="collapsed")
    if uploaded_file and st.button("Upload PDF", use_container_width=True):
        with st.spinner("Uploading..."):
            try:
                files = {
                    "file": (uploaded_file.name, uploaded_file, "application/pdf")
                }
                response = requests.post("http://localhost:8000/upload", files=files)
                result = response.json()

                if response.status_code == 200 and result.get("document_id"):
                    st.session_state.doc_id = result["document_id"]
                    st.success("✅ Upload successful!")
                else:
                    st.error(result.get("error", "Upload failed."))
            except Exception as e:
                st.error(f"Exception: {str(e)}")

# --- Q&A Section ---
if st.session_state.doc_id:
    st.markdown("### 💬 Ask Questions")

    for msg in st.session_state.chat_history:
        role_class = "user-msg" if msg["role"] == "user" else "bot-msg"
        st.markdown(f"<div class='message {role_class}'>{msg['content']}</div>", unsafe_allow_html=True)

    question = st.text_input("Ask your question:", placeholder="e.g., What is the summary?")
if st.button("Send", use_container_width=True) and question.strip():
    st.session_state.chat_history.append({"role": "user", "content": question})

    with st.spinner("Thinking..."):
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

else:
    st.info("📌 Please upload a PDF to start asking questions.")
