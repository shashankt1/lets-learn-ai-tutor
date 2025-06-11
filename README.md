# 🧠 Let's Learn - AI Tutor

A personalized AI-powered tutoring assistant built with **FastAPI**, **Streamlit**, **Whisper**, **ChromaDB**, and **LLaMA/Mistral**, designed to help students learn better by asking questions via text or audio — tailored to their age and understanding level.

---

## 🚀 Features

- 📁 Upload learning material (PDF, TXT, MP3, WAV, M4A)
- 🔍 Converts audio to text using **Whisper**
- 🧠 Retrieves context using **ChromaDB + Sentence Transformers**
- 💬 Answers based on student’s **age and learning level**
- 🗣️ Accepts both **text and voice questions**
- 🎛️ Built with modular backend (FastAPI) and clean frontend (Streamlit)
- 💾 Local vector store using **FAISS** and **Pickle**
- 🌐 CORS-enabled and ready for deployment

---

## 🖼️ Project Structure

lets-learn/
│
├── backend/
│ ├── main.py # FastAPI backend routes
│ ├── agent.py # RAG + prompt building logic
│ ├── file_processor.py # File parsing and chunking
│ ├── whisper_transcriber.py # Whisper audio transcriber
│ └── mistral_loader.py # LLM wrapper (e.g., Mistral, LLaMA)
│
├── frontend/
│ └── app.py # Streamlit frontend
│
├── vectorstore/
│ ├── index.faiss # FAISS vector DB
│ └── index.pkl # Chunk metadata
│
├── db/
│ └── db_handler.py # Log uploads / SQLite setup
│
├── data/uploads/ # Uploaded learning material
│
├── memory.json # Optional memory/log file
├── .env # API keys or environment variables
└── README.md # You're here.

yaml
Copy
Edit

---

## 🛠️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/shashankt1/lets-learn-ai-tutor.git
cd lets-learn-ai-tutor
2. Create virtual environment & install dependencies
bash
Copy
Edit
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
3. Run FastAPI backend
bash
Copy
Edit
cd backend
uvicorn main:app --reload --port 8010
4. Run Streamlit frontend
bash
Copy
Edit
cd ../frontend
streamlit run app.py
📦 Dependencies
fastapi, uvicorn

streamlit

openai-whisper

sentence-transformers

faiss-cpu

pydantic, requests, python-multipart

sqlite3 (for upload tracking)

💡 How It Works
Upload Material: PDFs and audio are converted to text and chunked.

Embed Chunks: Stored in FAISS with metadata.

Ask Question: User submits a question + age.

Retrieve & Answer: Relevant chunks are retrieved, styled prompt is built, and LLM answers it accordingly.

📚 Use Cases
AI tutor for school students

Educational chatbot in classrooms

Voice-based learning assistant

Personal study assistant for kids

📌 TODO / Improvements
✅ Audio-to-question flow with Whisper

✅ Age-based prompt styling

 File deletion + management

 Session history tracking

 Multi-language support

 HuggingFace Spaces / Docker deployment

🧑‍💻 Author
Shashank Tiwari
