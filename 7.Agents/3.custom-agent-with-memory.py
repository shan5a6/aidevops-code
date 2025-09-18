# ====================================================
# LangChain + Groq + FAISS + Custom Tool + Chat Agent with Memory
# ====================================================

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())  # ✅ Loads GROQ_API_KEY from .env

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from langchain_groq import ChatGroq
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain.tools import BaseTool
from typing import Optional
from langchain.callbacks.manager import AsyncCallbackManagerForToolRun, CallbackManagerForToolRun

# ====================================================
# Step 1: Load & Split Documents
# ====================================================
print("\n🔹 Loading documents...")
loader = TextLoader("/root/aidevops/aidevops-langchain/6.Retrival-Augumented-Generation/bella_vista.txt")
docs = loader.load()
print(f"✅ Loaded {len(docs)} document(s)")

print("\n🔹 Splitting documents into chunks...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
documents = text_splitter.split_documents(docs)
print(f"✅ Created {len(documents)} chunks")

# ====================================================
# Step 2: Create Embeddings & FAISS
# ====================================================
print("\n🔹 Creating embeddings & FAISS vectorstore...")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(documents, embeddings)
vectorstore.save_local("index")
print("✅ FAISS index created and saved locally")

# ====================================================
# Step 3: Define Custom Tool for Retrieval
# ====================================================
class CustomSearchTool(BaseTool):
    name: str = "restaurant_search"
    description: str = "Use this tool to answer any questions about Bella Vista restaurant (hours, menu, cuisine)."

    def _run(self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        docs = retriever.invoke(query)
        return "\n".join(doc.page_content for doc in docs)

    async def _arun(self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        raise NotImplementedError("Async not supported yet.")

# ====================================================
# Step 4: Initialize LLM
# ====================================================
print("\n🔹 Initializing Groq LLM...")
llm = ChatGroq(
    model="llama-3.3-70b-versatile",  # ✅ Newest Groq model
    temperature=0,
    max_tokens=512
)

# ====================================================
# Step 5: Add Conversation Memory
# ====================================================
memory = ConversationBufferMemory(
    memory_key="chat_history",       # Used by agent to maintain context
    return_messages=True
)

# ====================================================
# Step 6: Custom System Prompt (ReAct Format)
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
# Step 7: Create Chat Agent
# ====================================================
print("\n🔹 Initializing Chat Agent with Memory...")
tools = [CustomSearchTool()]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    memory=memory,                       # ✅ Enables conversational memory
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    max_iterations=3,
    handle_parsing_errors=True,
    agent_kwargs={"system_message": system_prompt}
)

# ====================================================
# Step 8: Start Interactive Chat
# ====================================================
print("\n✅ Chat Agent is ready! Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("👋 Goodbye! Chat ended.")
        break

    try:
        response = agent.invoke({"input": user_input})
        print(f"AI: {response['output']}")
    except Exception as e:
        print(f"⚠️ Error: {e}")
