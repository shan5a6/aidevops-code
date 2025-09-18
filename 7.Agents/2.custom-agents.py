# ====================================================
# LangChain + Groq + FAISS + Custom Tool + Agent (Improved)
# ====================================================

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())  # Load .env with GROQ_API_KEY

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from langchain_groq import ChatGroq
from langchain.agents import initialize_agent, AgentType
from langchain.tools import BaseTool
from typing import Optional
from langchain.callbacks.manager import AsyncCallbackManagerForToolRun, CallbackManagerForToolRun

# ====================================================
# Step 1: Load and Prepare Documents
# ====================================================
print("\n🔹 Loading documents...")
loader = TextLoader("/root/aidevops/aidevops-langchain/6.Retrival-Augumented-Generation/bella_vista.txt")
docs = loader.load()
print(f"✅ Loaded {len(docs)} documents")

# ====================================================
# Step 2: Split into Chunks
# ====================================================
print("\n🔹 Splitting documents into chunks...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
documents = text_splitter.split_documents(docs)
print(f"✅ Created {len(documents)} chunks")

# ====================================================
# Step 3: Create Embeddings & FAISS
# ====================================================
print("\n🔹 Creating embeddings & FAISS vectorstore...")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(documents, embeddings)
vectorstore.save_local("index")
print("✅ FAISS index created and saved locally")

# ====================================================
# Step 4: Define Custom Tool
# ====================================================
class CustomSearchTool(BaseTool):
    name: str = "restaurant_search"
    description: str = "Use this tool to answer any questions about Bella Vista restaurant (hours, menu, cuisine)."

    def _run(self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        retriever = vectorstore.as_retriever()
        docs = retriever.invoke(query)
        return "\n".join(doc.page_content for doc in docs)

    async def _arun(self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        raise NotImplementedError("Async not supported yet.")

# ====================================================
# Step 5: Load Groq LLM
# ====================================================
print("\n🔹 Initializing Groq LLM...")
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    max_tokens=512
)

# ====================================================
# Step 6: Custom System Prompt
# ====================================================
system_prompt = """You are a helpful AI assistant that must follow this strict format:

Thought: [Reasoning about the question]
Action: [Tool name OR 'Final Answer']
Action Input: [Input to the tool OR your final answer text]

❌ Never output multiple 'Action:' lines.
❌ Never say "Action: None needed".
✅ If you can answer directly, use:

Thought: I can answer directly.
Action: Final Answer
Action Input: [Your answer here]

Keep answers short and factual.
"""

# ====================================================
# Step 7: Create Agent
# ====================================================
print("\n🔹 Initializing Agent...")
tools = [CustomSearchTool()]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    max_iterations=3,  # ✅ Allow multiple retries
    handle_parsing_errors=True,
    agent_kwargs={"system_message": system_prompt}  # ✅ Better prompt control
)

# ====================================================
# Step 8: Ask Questions
# ====================================================
print("\n🔹 Asking Questions...")

try:
    response_1 = agent.invoke({"input": "When does Bella Vista open on Sunday?"})
except Exception as e:
    response_1 = {"output": f"⚠️ Could not get answer: {e}"}

try:
    response_2 = agent.invoke({"input": "What kind of food does Bella Vista serve?"})
except Exception as e:
    response_2 = {"output": f"⚠️ Could not get answer: {e}"}

print("\n--- FINAL ANSWERS ---")
print("🕒 Opening Hours (Sunday):", response_1["output"])
print("🍽 Cuisine Info:", response_2["output"])
