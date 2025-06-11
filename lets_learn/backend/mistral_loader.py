from llama_cpp import Llama
from db.db_handler import get_relevant_chunks
import os
import logging

# 🔹 Setup logging for better debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔹 Load LLaMA/Mistral model
model_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "llm_models", "mistral-7b-instruct-v0.1.Q4_K_M.gguf")
)

if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found at: {model_path}")

llm = Llama(
    model_path=model_path,
    n_ctx=2048,
    n_threads=os.cpu_count() or 4,
    use_mlock=True,
    verbose=False
)

# 🔹 Prompt template
def build_prompt(question: str, context: str) -> str:
    return f"""### Instruction:
You are an AI tutor. Your student is {"age"} years old.
Use the following material to answer their question in a simple, child-friendly way.

### Context:
{context}

### Question:
{question}

### Answer:
"""

# 🔹 Answering function with fallback
def generate_response(question: str) -> str:
    try:
        context_chunks = get_relevant_chunks(question)
        context = "\n".join(context_chunks[:5])  # Limit context to prevent overrun
        prompt = build_prompt(question, context)

        logger.info("Generated prompt sent to LLaMA.")

        output = llm(
            prompt=prompt,
            max_tokens=512,
            temperature=0.7,
            top_p=0.9,
            stop=["###"],
            echo=False
        )

        response = output["choices"][0]["text"].strip()
        return response or "I'm sorry, I couldn't generate a response."

    except Exception as e:
        logger.exception("❌ Error generating response.")
        return f"An error occurred while generating the answer: {str(e)}"
