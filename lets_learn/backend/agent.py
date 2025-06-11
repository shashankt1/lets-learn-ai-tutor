from backend.mistral_loader import generate_response
import pickle
import faiss
import os
import json

EMBEDDING_DIM = 384
VECTORSTORE_PATH = "../vectorstore/index.faiss"
METADATA_PATH = "../vectorstore/index.pkl"

# Load FAISS index and metadata
def load_vectorstore():
    if not os.path.exists(VECTORSTORE_PATH) or not os.path.exists(METADATA_PATH):
        return None, []
    index = faiss.read_index(VECTORSTORE_PATH)
    with open(METADATA_PATH, "rb") as f:
        metadata = pickle.load(f)
    return index, metadata


from sentence_transformers import SentenceTransformer
embedder = SentenceTransformer("all-MiniLM-L6-v2")

def get_relevant_chunks(query):
    index, metadata = load_vectorstore()
    if index is None:
        return []
    vec = embedder.encode([query])
    D, I = index.search(vec, k=3)
    return [metadata[i] for i in I[0] if i < len(metadata)]

def style_prompt(question, chunks, age):
    context = "\n---\n".join(chunks)
    if age < 10:
        return f"Explain this like I'm a kid using stories and simple words.\nQuestion: {question}\nContext:\n{context}"
    elif 10 <= age < 15:
        return f"Explain this clearly and in a friendly way suitable for a teenager.\nQuestion: {question}\nContext:\n{context}"
    else:
        return f"Answer the following question concisely and logically.\nQuestion: {question}\nContext:\n{context}"

def answer_question(question, age):
    chunks = get_relevant_chunks(question)
    prompt = style_prompt(question, chunks, age)
    return generate_response(prompt)