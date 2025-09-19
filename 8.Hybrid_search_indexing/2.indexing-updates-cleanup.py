# ====================================================
# LangChain + PGVector + Document Updates + Cleanup
# ====================================================
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_postgres.vectorstores import PGVector
from langchain.indexes import SQLRecordManager, index
from langchain.schema import Document
# ====================================================
# Step 1: Setup Embeddings & PGVector
# ====================================================
print("\n🔹 Setting up embeddings...")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
CONNECTION_STRING = "postgresql+psycopg://admin:admin@127.0.0.1:5433/vectordb"
COLLECTION_NAME = "vectordb"
print("🔹 Connecting to PGVector...")
vectorstore = PGVector(
    collection_name=COLLECTION_NAME,
    connection=CONNECTION_STRING,
    embeddings=embeddings,
)
namespace = f"pgvector/{COLLECTION_NAME}"
record_manager = SQLRecordManager(namespace, db_url=CONNECTION_STRING)
record_manager.create_schema()
# ====================================================
# Step 2: Load and Index Documents
# ====================================================
print("\n🔹 Loading documents...")
loader = TextLoader("/root/aidevops/aidevops-langchain/8.Hybrid_search_indexing/bella_vista.txt")
documents = loader.load()
print("🔹 Splitting documents...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
docs = text_splitter.split_documents(documents)
print(f"✅ {len(docs)} chunks created")
print("🔹 Indexing initial documents...")
index(docs, record_manager, vectorstore, cleanup=None, source_id_key="source")
print("✅ Initial indexing complete")
# ====================================================
# Step 3: Simulate Updates
# ====================================================
print("\n🔹 Simulating updates...")
docs[1].page_content = "updated"
del docs[2]
docs.append(Document(page_content="new content", metadata={"source": "important"}))
print("🔹 Re-indexing with no cleanup (keeps deleted docs)...")
index(docs, record_manager, vectorstore, cleanup=None, source_id_key="source")
# ====================================================
# Step 4: Incremental Cleanup
# ====================================================
print("\n🔹 Performing incremental cleanup (removes deleted docs)...")
docs[1].page_content = "updated again"
del docs[3]
docs.append(Document(page_content="more new content", metadata={"source": "important"}))
index(docs, record_manager, vectorstore, cleanup="incremental", source_id_key="source")
print("✅ Incremental cleanup complete")
# ====================================================
# Step 5: Full Cleanup
# ====================================================
print("\n🔹 Performing full cleanup (reset index completely)...")
index([], record_manager, vectorstore, cleanup="full", source_id_key="source")
print("✅ Full cleanup done")
