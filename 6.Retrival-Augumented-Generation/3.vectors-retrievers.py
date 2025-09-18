# =========================================================
# 📌 LANGCHAIN - VECTORS & RETRIEVERS (STEP-BY-STEP)
# =========================================================

# 1️⃣ Load environment variables (good practice for future API keys)
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# 2️⃣ Load the document
from langchain_community.document_loaders import TextLoader

loader = TextLoader("/root/aidevops/aidevops-langchain/6.Retrival-Augumented-Generation/bella_vista.txt")
docs = loader.load()

print(f"✅ Loaded {len(docs)} document(s)")
print("Sample Document:", docs[0])

# ---------------------------------------------------------

# 3️⃣ Split document into smaller chunks
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,  # number of characters in one chunk
    chunk_overlap=20 # overlap to avoid losing context
)

documents = text_splitter.split_documents(docs)

print(f"✅ Created {len(documents)} chunks")
print("Sample Chunk:", documents[0])

# ---------------------------------------------------------

# 4️⃣ Create embeddings (Convert text → vectors)
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Test embedding for a query
query_vector = embeddings.embed_query("What are the opening hours?")
print(f"✅ Query vector length: {len(query_vector)}")

# ---------------------------------------------------------

# 5️⃣ Store chunks in FAISS vector database

# ================== 
# rm -rf /root/miniconda3
# wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
# bash Miniconda3-latest-Linux-x86_64.sh
# source ~/.bashrc
# conda create -n aidevops python=3.12 -y
# conda activate aidevops
# conda install -c conda-forge faiss-cpu -y
# pip install langchain-community sentence-transformers

# ================== 

from langchain_community.vectorstores import FAISS

vectorstore = FAISS.from_documents(documents, embeddings)
vectorstore.save_local("bella_vista_index")

print("✅ Vectorstore created and saved locally")

# ---------------------------------------------------------

# 6️⃣ Load the saved vectorstore and create retriever
vectorstore = FAISS.load_local("bella_vista_index", embeddings, allow_dangerous_deserialization=True)
retriever = vectorstore.as_retriever()

# ---------------------------------------------------------

# 7️⃣ Retrieve relevant chunks for a query
print("\n🔎 Example Query: When are the opening hours?")
docs = retriever.invoke("When are the opening hours?")

print("\n✅ Retrieved Chunks:")
for i, d in enumerate(docs, start=1):
    print(f"\nChunk {i}:")
    print(d.page_content)

# ---------------------------------------------------------

# 8️⃣ Try another query
print("\n🔎 Example Query: Do you offer vegan dishes?")
docs = retriever.invoke("Do you offer vegan dishes?")

print("\n✅ Retrieved Chunks:")
for i, d in enumerate(docs, start=1):
    print(f"\nChunk {i}:")
    print(d.page_content)

# =========================================================
# END OF SCRIPT
# =========================================================
