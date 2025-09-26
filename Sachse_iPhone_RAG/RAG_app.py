# --- Suppress noisy logs and warnings ---
import logging
import warnings
from transformers import logging as hf_logging

# Set specific loggers to ERROR level
logging.getLogger("langchain.text_splitter").setLevel(logging.ERROR)

# Silence Hugging Face transformers logs
hf_logging.set_verbosity_error()

# Filter out generic Python warnings
warnings.filterwarnings("ignore")

# --- Load OpenAI API key from .env ---
import os
from dotenv import load_dotenv
from openai import OpenAI  # UPDATED: use new OpenAI client

# Load environment variables from .env in the current directory
load_dotenv()

# Initialize OpenAI client (replaces openai.api_key = ...)  # UPDATED
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- RAG Parameters ---

# Text splitting parameters
chunk_size = 100 #500 initially
chunk_overlap = 50

# Embedding model (bi-encoder)
model_name = "sentence-transformers/all-distilroberta-v1"

# Retrieval parameters
top_k = 20

# Re-ranking parameters
cross_encoder_name = "cross-encoder/ms-marco-MiniLM-L-6-v2"
top_m = 8

# --- Load pre-scraped document ---
DOC_PATH = "Selected_Document.txt"

try:
    with open(DOC_PATH, "r", encoding="utf-8") as f:
        text = f.read()
    print(f"✅ Loaded document: {DOC_PATH} ({len(text)} characters)")
except FileNotFoundError:
    print(f"❌ {DOC_PATH} not found. Make sure to run your extractor first.")
    text = ""

# --- Split text into chunks ---
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Define the splitter with your parameters
splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap,
    separators=["", "\n", " ", ""]
)

# Perform the split
chunks = splitter.split_text(text)

print(f"✅ Split document into {len(chunks)} chunks.")

# --- Embed chunks and build FAISS index ---
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss  # make sure faiss-cpu is installed

# Load the embedding model
embedder = SentenceTransformer(model_name)

# Encode the chunks (progress bar hidden)
embeddings = embedder.encode(chunks, show_progress_bar=False)

# Ensure float32 dtype for FAISS
embeddings = np.array(embeddings, dtype="float32")

# Initialize FAISS index
dim = embeddings.shape[1]
faiss_index = faiss.IndexFlatL2(dim)

# Add embeddings to the index
faiss_index.add(embeddings)

print(f"✅ Built FAISS index with {faiss_index.ntotal} vectors of dimension {dim}.")

# --- Retrieve nearest chunks from FAISS ---
from typing import List

def retrieve_chunks(question: str, k: int = top_k) -> List[str]:
    """
    Encode the question, search the FAISS index for top-k neighbors,
    and return the corresponding text chunks.

    Assumes the following exist in the global namespace:
      - embedder: SentenceTransformer
      - faiss_index: faiss.Index
      - chunks: List[str]
      - top_k: int (default used for k)
    """
    # Encode query with the bi-encoder (no progress bar for interactivity)
    q_vec = embedder.encode([question], show_progress_bar=False)

    # Convert to float32 NumPy array for FAISS
    q_arr = np.array(q_vec, dtype="float32")

    # Search FAISS for the top-k nearest neighbors
    D, I = faiss_index.search(q_arr, k)  # distances, indices

    # Map indices back to text chunks
    idxs = I[0].tolist()
    return [chunks[i] for i in idxs if 0 <= i < len(chunks)]

# --- Cross-encoder re-ranking ---
import re
from typing import List
from sentence_transformers import CrossEncoder

# Initialize the cross-encoder reranker (uses the name defined earlier)
reranker = CrossEncoder(cross_encoder_name)

def dedupe_preserve_order(items: List[str]) -> List[str]:
    """Remove exact duplicates while preserving first occurrence."""
    seen = set()
    out = []
    for s in items:
        if s not in seen:
            seen.add(s)
            out.append(s)
    return out

def _normalize_ws(s: str) -> str:
    """Normalize whitespace to reduce near-duplicates."""
    return re.sub(r"\s+", " ", s).strip()

def rerank_chunks(question: str, candidate_chunks: List[str], m: int = top_m) -> List[str]:
    """
    Score (question, chunk) pairs with a cross-encoder and return the best m.

    Notes:
      - Does NOT re-encode with the bi-encoder; only uses the cross-encoder for scoring.
      - Assumes cross_encoder_name and top_m are already defined in the program.
    """
    # Normalize to avoid scoring redundant near-duplicates
    cleaned = [_normalize_ws(c) for c in candidate_chunks if c and c.strip()]

    if not cleaned:
        return []

    # Create pairs and score
    pairs = [(question, c) for c in cleaned]
    scores = reranker.predict(pairs)  # higher = more relevant

    # Sort by score (desc) and select top m
    ranked = sorted(zip(cleaned, scores), key=lambda x: x[1], reverse=True)[:m]
    selected = [c for c, _ in ranked]

    # Light dedupe to avoid repeats
    return dedupe_preserve_order(selected)


# --- Q&A with OpenAI Chat Completions ---

def _build_qa_prompts(question: str, context: str) -> tuple[str, str]:
    """
    Helper to construct the system and user prompts for Chat Completions.
    """
    system_prompt = (
        "You are a knowledgeable assistant that answers questions based on the provided context. "
        "If the answer is not in the context, say you don’t know."
    )

    user_prompt = f"""Context:
{context}

Question: {question}

Answer:"""

    return system_prompt, user_prompt


def answer_question(question: str) -> str:
    """
    Retrieve candidate chunks, re-rank them, and synthesize an answer
    using the OpenAI Chat Completions API.
    """
    candidates = retrieve_chunks(question)
    relevant_chunks = rerank_chunks(question, candidates, m=top_m)
    context = "\n\n".join(relevant_chunks)
    system_prompt, user_prompt = _build_qa_prompts(question, context)

    # UPDATED: new client-based call
    resp = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ],
        max_completion_tokens=500,
    )
    return resp.choices[0].message.content.strip()


# --- Interactive loop for Q&A ---
if __name__ == "__main__":
    print("Enter 'exit' or 'quit' to end.")
    while True:
        try:
            question = input("Your question: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Bye!")
            break

        if question.lower() in ("exit", "quit"):
            print("👋 Bye!")
            break

        if not question:
            continue

        try:
            answer = answer_question(question)
            print("Answer:", answer)
        except Exception as e:
            print("⚠️ Error while answering:", e)
