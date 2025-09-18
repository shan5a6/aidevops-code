# =========================================================
# LANGCHAIN - COMPLETE RAG PIPELINE WITH GROQ
# =========================================================

# 1️⃣ Load environment variables (good practice for future API keys)
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# ---------------------------------------------------------
# 2️⃣ Load the document
from langchain_community.document_loaders import TextLoader

# Make sure you have a file named 'bella_vista.txt' in this path
loader = TextLoader("/root/aidevops/aidevops-langchain/6.Retrival-Augumented-Generation/bella_vista.txt")
docs = loader.load()

print(f"✅ Loaded {len(docs)} document(s)")
print("Sample Document:", docs[0])

# ---------------------------------------------------------
# 3️⃣ Split document into smaller chunks
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,  # number of characters per chunk
    chunk_overlap=20 # overlap to avoid losing context
)

documents = text_splitter.split_documents(docs)
print(f"✅ Created {len(documents)} chunks")
print("Sample Chunk:", documents[0])

# ---------------------------------------------------------
# 4️⃣ Create embeddings (Convert text → vectors)
from langchain_huggingface import HuggingFaceEmbeddings

# Using open-source, lightweight embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Test embedding for a query
query_vector = embeddings.embed_query("What are the opening hours?")
print(f"✅ Query vector length: {len(query_vector)}")

# ---------------------------------------------------------
# 5️⃣ Store chunks in FAISS vector database
from langchain_community.vectorstores import FAISS

vectorstore = FAISS.from_documents(documents, embeddings)
vectorstore.save_local("bella_vista_index")
print("✅ Vectorstore created and saved locally")

# ---------------------------------------------------------
# 6️⃣ Load the saved vectorstore and create retriever
vectorstore = FAISS.load_local("bella_vista_index", embeddings, allow_dangerous_deserialization=True)
retriever = vectorstore.as_retriever()

# ---------------------------------------------------------
# 7️⃣ Initialize Groq LLM and Prompt Template
from langchain_groq import ChatGroq
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.prompts import PromptTemplate

# Define the prompt template
prompt_template = """You are a helpful assistant for our restaurant.

{context}

Question: {input}
Answer here:"""

PROMPT = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "input"]
)

# Initialize Groq LLM
llm = ChatGroq(model="llama-3.3-70b-versatile")

# Create documents chain
combine_docs_chain = create_stuff_documents_chain(llm, PROMPT)

# Create retrieval chain
qa = create_retrieval_chain(
    retriever=retriever,
    combine_docs_chain=combine_docs_chain
)

# ---------------------------------------------------------
# 8️⃣ Example Queries
print("\n🔎 Example Query: When are the opening hours?")
result1 = qa.invoke({"input": "When are the opening hours on Sunday?"})
# print(result1)
print(result1.get("answer"))

print("\n🔎 Example Query: Do you offer vegetarian or vegan options?")
result2 = qa.invoke({"input": "Do you offer vegetarian or vegan options?"})
# print(result2)
print(result2.get("answer"))

print("\n🔎 Example Query: Can I book a private event?")
result3 = qa.invoke({"input": "Can I book a private event?"})
# print(result3)
print(result3.get("answer"))

# =========================================================
# END OF SCRIPT
# =========================================================
