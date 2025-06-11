import os
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import faiss
import pickle

from typing import List

from db.db_handler import save_to_vectorstore

EMBEDDING_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

VECTOR_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../vectorstore/"))
UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/uploads/"))

CHUNK_SIZE = 500


def read_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    return text


def read_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def split_text(text: str) -> List[str]:
    return [text[i:i + CHUNK_SIZE] for i in range(0, len(text), CHUNK_SIZE)]


def embed_chunks(chunks: List[str]):
    return EMBEDDING_MODEL.encode(chunks)


def store_embeddings(chunks: List[str], embeddings, filename: str):
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    with open(os.path.join(VECTOR_DIR, "index.pkl"), "wb") as f:
        pickle.dump(chunks, f)

    faiss.write_index(index, os.path.join(VECTOR_DIR, "index.faiss"))


# 🔹 Main entry point for FastAPI to call when user uploads a file

def process_file(file_path: str):
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == ".pdf":
        text = read_pdf(file_path)
    elif ext == ".txt":
        text = read_txt(file_path)
    else:
        raise ValueError("Unsupported file format")

    chunks = split_text(text)
    embeddings = embed_chunks(chunks)
    store_embeddings(chunks, embeddings, file_path)

    # Save to ChromaDB vectorstore for search
    save_to_vectorstore(chunks, metadata={"source": os.path.basename(file_path)})

    return chunks
