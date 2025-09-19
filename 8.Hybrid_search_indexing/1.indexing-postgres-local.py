# ====================================================
# LangChain + Groq + HuggingFace Embeddings + PGVector
# ====================================================

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())  # ✅ Loads secrets like GROQ_API_KEY

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_postgres.vectorstores import PGVector
from langchain.indexes import SQLRecordManager, index

# ====================================================
# Step 1: Load and Split Documents
# ====================================================
print("\n🔹 Loading documents...")
loader = TextLoader("/root/aidevops/aidevops-langchain/8.Hybrid_search_indexing/bella_vista.txt")
documents = loader.load()
print(f"✅ Loaded {len(documents)} document(s)")

print("\n🔹 Splitting into chunks...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
docs = text_splitter.split_documents(documents)
print(f"✅ Created {len(docs)} chunks")

# ====================================================
# Step 2: Create Embeddings
# ====================================================
print("\n🔹 Creating embeddings...")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
print("✅ Embeddings model loaded")

# ====================================================
# Step 3: Connect to PGVector
# ====================================================
CONNECTION_STRING = "postgresql+psycopg://admin:admin@127.0.0.1:5433/vectordb"
COLLECTION_NAME = "vectordb"

vectorstore = PGVector(
    collection_name=COLLECTION_NAME,
    connection=CONNECTION_STRING,
    embeddings=embeddings,
)
print("✅ Connected to PGVector")

# ====================================================
# Step 4: Manage Records & Index
# ====================================================
from langchain.indexes import SQLRecordManager, index

namespace = f"pgvector/{COLLECTION_NAME}"
record_manager = SQLRecordManager(namespace, db_url=CONNECTION_STRING)
record_manager.create_schema()  # ✅ Create schema if not exists

print("\n🔹 Indexing documents into PGVector...")
index(docs, record_manager, vectorstore, cleanup="full", source_id_key="source")
print("✅ Documents indexed successfully")

# print("==== printing data before update operation ==== ")
# print(docs[1].page_content)
# print("==== printing data after update operation ==== ")
# docs[1].page_content = "updated with new content"
# index(docs, record_manager, vectorstore, cleanup=None, source_id_key="source")
# print(docs[1].page_content)

