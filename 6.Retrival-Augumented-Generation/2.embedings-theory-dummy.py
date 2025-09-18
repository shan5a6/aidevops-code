# ========================================
# 1️⃣ Setup & Install Required Libraries
# ========================================
# pip install langchain langchain-community sentence-transformers numpy python-dotenv

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())  # Load .env file (good practice for API keys, even if we don't use one here)

# ========================================
# 2️⃣ Import HuggingFace Embeddings (Free & Local)
# ========================================
from langchain_community.embeddings import HuggingFaceEmbeddings

# Using a small, fast model suitable for demos
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# ========================================
# 3️⃣ Create Some Example Texts
# ========================================
text_1 = "The solar system consists of the Sun and the objects that orbit it"
text_2 = "The solar system consists of the Sun and the objects that orbit it"
text_3 = "Planets, asteroids, and comets are part of our solar system."
text_4 = "I love baking chocolate chip cookies on weekends."

# ========================================
# 4️⃣ Generate Embeddings
# ========================================
embedding1 = embeddings.embed_query(text_1)
embedding2 = embeddings.embed_query(text_2)
embedding3 = embeddings.embed_query(text_3)
embedding4 = embeddings.embed_query(text_4)

print(f"✅ Length of embedding vector: {len(embedding1)}")  # Typically 384 or 768 depending on model
print(f"✅ First 5 values of embedding1: {embedding1[:5]}")

# ========================================
# 5️⃣ Cosine Similarity Function
# ========================================
import numpy as np

def cosine_similarity(A, B):
    """Compute cosine similarity between two vectors A and B."""
    dot_product = np.dot(A, B)
    norm_a = np.linalg.norm(A)
    norm_b = np.linalg.norm(B)
    return dot_product / (norm_a * norm_b)

# ========================================
# 6️⃣ Calculate Similarities
# ========================================
sim_1_2 = cosine_similarity(embedding1, embedding2)
sim_1_3 = cosine_similarity(embedding1, embedding3)
sim_3_4 = cosine_similarity(embedding3, embedding4)

print("\n=== Cosine Similarity Results ===")
print(f"Similarity between text_1 and text_2 (exact same sentence): {sim_1_2:.4f}")
print(f"Similarity between text_1 and text_3 (related topic): {sim_1_3:.4f}")
print(f"Similarity between text_3 and text_4 (completely different topic): {sim_3_4:.4f}")
