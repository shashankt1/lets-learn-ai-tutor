import streamlit as st
import requests
import os

BACKEND_URL = "http://localhost:8010"

st.set_page_config(page_title="AI Tutor", layout="centered")
st.title("🤖 Let's Learn - AI Tutor")

# Optional: check backend health
try:
    health = requests.get(f"{BACKEND_URL}/health")
    if health.status_code != 200:
        st.error("🚨 Backend is not healthy. Please check the FastAPI server.")
except Exception:
    st.error("⚠️ Cannot connect to backend. Is FastAPI running on port 8010?")
    st.stop()

# Upload Material
st.sidebar.header("📁 Upload Learning Material")
uploaded_file = st.sidebar.file_uploader(
    "Upload PDF, TXT, MP3, WAV, M4A", type=["pdf", "txt", "mp3", "wav", "m4a"]
)

if uploaded_file is not None:
    with st.spinner("🔄 Uploading and processing file..."):
        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
        try:
            response = requests.post(f"{BACKEND_URL}/upload", files=files)
            if response.status_code == 200:
                data = response.json()
                st.success(f"✅ Processed {uploaded_file.name}. Chunks embedded: {data['chunks']}")
            else:
                st.error(f"❌ Error: {response.json().get('error')}")
        except Exception as e:
            st.error(f"❌ Failed to reach backend: {e}")

# Age selection
st.sidebar.header("🎓 Learner Profile")
age = st.sidebar.slider("Student Age", min_value=4, max_value=18, value=10)

# Text Q&A
st.header("📚 Ask a Question")
question = st.text_input("Type your question:")

if st.button("Get Answer") and question:
    with st.spinner("🧠 Thinking..."):
        try:
            response = requests.post(f"{BACKEND_URL}/ask", data={"age": age, "question": question})
            if response.status_code == 200:
                st.markdown("#### Answer:")
                st.success(response.json().get("answer"))
            else:
                st.error(f"❌ Error: {response.json().get('error')}")
        except Exception as e:
            st.error(f"⚠️ Backend error: {e}")

# Audio Q&A
st.sidebar.header("🎤 Ask with Audio")
audio_file = st.sidebar.file_uploader(
    "Upload voice question (MP3, WAV, M4A)", type=["mp3", "wav", "m4a"], key="audio"
)

if audio_file is not None:
    with st.spinner("🔊 Transcribing and answering..."):
        files = {"file": (audio_file.name, audio_file.getvalue())}
        try:
            response = requests.post(
                f"{BACKEND_URL}/ask_audio", data={"age": age}, files=files
            )
            if response.status_code == 200:
                result = response.json()
                st.markdown("#### Transcribed Question:")
                st.info(result.get("question"))
                st.markdown("#### Answer:")
                st.success(result.get("answer"))
            else:
                st.error(f"❌ Error: {response.json().get('error')}")
        except Exception as e:
            st.error(f"⚠️ Failed to reach backend: {e}")

# Footer
st.markdown("---")
st.caption("Built with 💡 FastAPI + LLaMA + ChromaDB + Whisper + Streamlit")