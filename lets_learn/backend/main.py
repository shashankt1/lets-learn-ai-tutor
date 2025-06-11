from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os

from backend.agent import answer_question
from backend.file_processor import process_file
from backend.whisper_transcriber import transcribe_audio
from db.db_handler import init_db, log_upload

UPLOAD_FOLDER = "../data/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = FastAPI()

# Initialize DB at startup
@app.on_event("startup")
def startup_event():
    init_db()

# Enable CORS (adjust allow_origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_ext = os.path.splitext(file.filename)[1].lower()
    save_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(save_path, "wb") as f:
        f.write(await file.read())

    try:
        if file_ext in [".pdf", ".txt"]:
            status = process_file(save_path)
        elif file_ext in [".mp3", ".wav", ".m4a"]:
            transcript = transcribe_audio(save_path)
            transcript_path = save_path + ".txt"
            with open(transcript_path, "w", encoding="utf-8") as f:
                f.write(transcript)
            status = process_file(transcript_path)
        else:
            return JSONResponse(
                content={"error": f"Unsupported file type: {file_ext}"},
                status_code=400,
            )

        log_upload(file.filename)

        return {
            "message": f"File '{file.filename}' successfully processed",
            "chunks": status
        }

    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500,
        )

@app.post("/ask")
async def ask_question(age: int = Form(...), question: str = Form(...)):
    try:
        response = answer_question(question, age)
        return {"answer": response}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/ask_audio")
async def ask_audio(file: UploadFile = File(...), age: int = Form(...)):
    try:
        audio_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(audio_path, "wb") as f:
            f.write(await file.read())

        question = transcribe_audio(audio_path)
        response = answer_question(question, age)

        return {"question": question, "answer": response}

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)