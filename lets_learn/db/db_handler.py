import sqlite3
from datetime import datetime
import os
import chromadb
from chromadb.utils import embedding_functions

# 📌 Define paths
DB_PATH = os.path.join(os.path.dirname(__file__), "meta.db")
VECTOR_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "vectorstore"))

# 🔹 Setup ChromaDB
embedding_fn = embedding_functions.DefaultEmbeddingFunction()
client = chromadb.PersistentClient(path=VECTOR_DIR)
collection = client.get_or_create_collection(name="learn_chunks", embedding_function=embedding_fn)

# 🔹 Initialize uploads DB
def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS uploads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# 🔹 Log a new upload
def log_upload(filename: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO uploads (filename, timestamp) VALUES (?, ?)",
        (filename, datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()

# 🔹 List all uploads
def list_uploads():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM uploads ORDER BY timestamp DESC")
    uploads = c.fetchall()
    conn.close()
    return uploads

# ✅ 🔹 Save chunks to ChromaDB vectorstore
def save_to_vectorstore(chunks: list[str], filename: str):
    ids = [f"{filename}_{i}" for i in range(len(chunks))]
    metadatas = [{"source": filename} for _ in chunks]
    collection.add(documents=chunks, ids=ids, metadatas=metadatas)

# 🔹 Retrieve top-k relevant chunks using semantic search
def get_relevant_chunks(query: str, top_k: int = 5):
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    return results["documents"][0] if results["documents"] else []