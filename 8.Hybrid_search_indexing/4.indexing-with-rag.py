# ====================================================
# LangChain + PGVector + Retriever + Groq LLM (RAG)
# ====================================================
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres.vectorstores import PGVector
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq

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
# Step 2: Index Documents (Run Once)
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
# Step 3: Setup Groq LLM
# ====================================================
print("\n🔹 Initializing Groq LLM...")
llm = ChatGroq(
    model="llama-3.3-70b-versatile",  # Powerful Groq LLM
    temperature=0,                   # Deterministic responses
    max_tokens=300
)

# ====================================================
# Step 4: Setup Retriever + QA Chain
# ====================================================
retriever = store.as_retriever(search_kwargs={"k": 3})

prompt_template = """
You are a helpful assistant that answers questions based on restaurant information.

Context:
{context}

Question:
{question}

Answer in a friendly and clear way, using only the information provided above.
"""

prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    chain_type_kwargs={"prompt": prompt},
    return_source_documents=True
)

# ====================================================
# Step 5: Ask Questions (Chatbot Mode)
# ====================================================
print("\n🔹 Asking Questions with RAG...")
questions = [
    "When does Bella Vista open on Sunday?",
    "What type of cuisine does Bella Vista serve?",
    "Do you offer vegetarian or vegan options?",
    "Can I book private events at Bella Vista?"
]

for q in questions:
    result = qa_chain.invoke({"query": q})
    print(f"\n❓ Question: {q}")
    print(f"💡 Answer: {result['result']}")
    for doc in result['source_documents']:
        print(f"📄 Source: {doc.metadata.get('source', 'N/A')}")
