# ====================================================
# LangChain + PGVector + Retriever Example (Groq Ready)
# ====================================================
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# ✅ Updated import (fix deprecation)
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres.vectorstores import PGVector
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter

# ====================================================
# Step 1: Setup Embeddings & Vector Store
# ====================================================
print("\n🔹 Setting up embeddings...")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

CONNECTION_STRING = "postgresql+psycopg://admin:admin@127.0.0.1:5433/vectordb"
COLLECTION_NAME = "vectordb"

print("🔹 Connecting to PGVector...")
store = PGVector(
    collection_name=COLLECTION_NAME,
    connection=CONNECTION_STRING,
    embeddings=embeddings,
)

# ====================================================
# Step 2: Index Documents (Only Once)
# ====================================================
print("\n🔹 Loading and indexing documents...")
loader = TextLoader("/root/aidevops/aidevops-langchain/8.Hybrid_search_indexing/bella_vista_new.txt")
docs = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
splits = text_splitter.split_documents(docs)

if splits:
    store.add_documents(splits)
    print(f"✅ Indexed {len(splits)} chunks into PGVector!")
else:
    print("⚠️ No documents found to index.")

# ====================================================
# Step 3: Similarity Search Examples
# ====================================================
print("\n🔹 Searching without filters...")
results = store.similarity_search_with_score("when does the restaurant open?")
for doc, score in results:
    print(f"Score: {score:.3f}, Content: {doc.page_content[:80]}...")

print("\n🔹 Searching with filter...")
results = store.similarity_search_with_score(
    "when does the restaurant open?",
    filter={"source": "/root/aidevops/aidevops-langchain/8.Hybrid_search_indexing/bella_vista_new.txt"},
)
for doc, score in results:
    print(f"Filtered Score: {score:.3f}, Content: {doc.page_content[:80]}...")

print("\n🔹 Searching with top-3 results...")
results = store.similarity_search_with_score(
    "Bella Vista cuisine",
    filter={"source": "/root/aidevops/aidevops-langchain/8.Hybrid_search_indexing/bella_vista_new.txt"},
    k=3,
)
for doc, score in results:
    print(f"Top-3 Score: {score:.3f}, Content: {doc.page_content[:80]}...")

# ====================================================
# Step 4: Using Retriever (Recommended)
# ====================================================
print("\n🔹 Using Retriever...")
retriever = store.as_retriever(search_kwargs={"k": 2})
docs = retriever.invoke("vegetarian options at Bella Vista")
for doc in docs:
    print(f"Retriever Result: {doc.page_content[:80]}...")

print("\n🔹 Using Retriever with Filter...")
retriever = store.as_retriever(
    search_kwargs={
        "k": 2,
        "filter": {"source": "/root/aidevops/aidevops-langchain/8.Hybrid_search_indexing/bella_vista_new.txt"},
    }
)
docs = retriever.invoke("book a private event")
for doc in docs:
    print(f"Retriever Filtered Result: {doc.page_content[:80]}...")
