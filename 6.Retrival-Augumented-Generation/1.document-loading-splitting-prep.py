# 📌 Step 1: Load Env Variables
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# 📌 Step 2: Load Text Data
from langchain_community.document_loaders import TextLoader
loader = TextLoader("/root/aidevops/aidevops-langchain/6.Retrival-Augumented-Generation/bella_vista.txt")
docs = loader.load()
print(f"Loaded {len(docs)} document(s)")

# 📌 Step 3: Split into Chunks
from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,  # small chunks for demo
    chunk_overlap=20
)
documents = text_splitter.split_documents(docs)
print(f"Created {len(documents)} chunks.")

# 📌 Step 4: Setup Groq LLM
from langchain_groq import ChatGroq
llm = ChatGroq(model="llama-3.3-70b-versatile")

# 📌 Step 5: Simple Question Answering
question = "What time do you open on Sundays?"
context = " ".join([doc.page_content for doc in documents])  # Combine chunks
final_prompt = f"Context: {context}\n\nQuestion: {question}\nAnswer in simple terms:"

response = llm.invoke(final_prompt)
print("\n--- Answer ---")
print(response.content)
