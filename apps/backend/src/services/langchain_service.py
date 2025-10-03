import os
import re
import numpy as np
from collections import Counter

# Try to load OpenAI if API key exists
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
USE_OPENAI = False
embeddings_model = None

if OPENAI_API_KEY:
    try:
        from langchain_openai import OpenAIEmbeddings
        embeddings_model = OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=OPENAI_API_KEY
        )
        USE_OPENAI = True
    except Exception:
        USE_OPENAI = False


def simple_vectorize(text: str):
    words = re.findall(r"\w+", text.lower())
    return Counter(words)


def compute_similarity(text1: str, text2: str) -> float:
    """
    Compute similarity between two texts.
    - Uses OpenAI embeddings if available
    - Otherwise falls back to simple word overlap
    """
    if USE_OPENAI and embeddings_model:
        try:
            vec1 = embeddings_model.embed_query(text1)
            vec2 = embeddings_model.embed_query(text2)

            v1 = np.array(vec1)
            v2 = np.array(vec2)

            score = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
            return round(float(score), 2)
        except Exception:
            # fallback if API quota error or any failure
            pass

    # --- fallback similarity (no API key or error) ---
    vec1 = simple_vectorize(text1)
    vec2 = simple_vectorize(text2)

    common = set(vec1.keys()) & set(vec2.keys())
    dot = sum(vec1[w] * vec2[w] for w in common)

    norm1 = np.sqrt(sum(v**2 for v in vec1.values()))
    norm2 = np.sqrt(sum(v**2 for v in vec2.values()))

    if norm1 == 0 or norm2 == 0:
        return 0.0

    score = dot / (norm1 * norm2)
    return round(float(score), 2)
