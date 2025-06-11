@echo off
REM Create the root folder
mkdir lets_learn
cd lets_learn

REM Create subfolders
mkdir frontend
mkdir backend
mkdir llm_models
mkdir vectorstore
mkdir data
mkdir data\uploads
mkdir db

REM Create files
type nul > frontend\app.py
type nul > frontend\utils.py
type nul > frontend\styles.css

type nul > backend\main.py
type nul > backend\agent.py
type nul > backend\mistral_loader.py
type nul > backend\file_processor.py
type nul > backend\whisper_transcriber.py

type nul > llm_models\mistral-7b.Q4_K_M.gguf

type nul > vectorstore\index.faiss
type nul > vectorstore\index.pkl

type nul > db\memory.json

type nul > requirements.txt
type nul > Dockerfile
type nul > README.md
type nul > .env

echo Project structure created successfully!
pause
