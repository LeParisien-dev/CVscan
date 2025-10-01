import os
from langchain_openai import OpenAIEmbeddings
import numpy as np

# Load API key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

embeddings_model = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=OPENAI_API_KEY
)

def compute_similarity(text1: str, text2: str) -> float:
    """
    Compute cosine similarity between embeddings of two texts.
    """
    vec1 = embeddings_model.embed_query(text1)
    vec2 = embeddings_model.embed_query(text2)

    v1 = np.array(vec1)
    v2 = np.array(vec2)

    # cosine similarity
    score = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    return round(float(score), 2)
