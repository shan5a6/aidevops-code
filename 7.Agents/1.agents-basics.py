# =========================================================
# 📌 LANGCHAIN - AGENTS WITH GROQ + TOOLS (STEP-BY-STEP)
# =========================================================

# 1️⃣ Load environment variables (for GROQ_API_KEY)
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# 2️⃣ Import Groq Chat Model (Instead of OpenAI)
from langchain_groq import ChatGroq

# 3️⃣ Import Agent & Tool Utilities
from langchain.agents import load_tools, initialize_agent, AgentType

# ---------------------------------------------------------
# 4️⃣ Initialize Groq LLM
# "llama-3.1-70b-versatile" is one of the best available models for reasoning
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# ---------------------------------------------------------
# 5️⃣ Load Tools (Here we use the LLM-Math tool)
tool_names = ["llm-math"]
tools = load_tools(tool_names, llm=llm)

print(f"✅ Loaded Tools: {[tool.name for tool in tools]}")

# ---------------------------------------------------------
# 6️⃣ Initialize the Agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # Uses ReAct loop
    verbose=True, # Show reasoning steps in console (great for learning!)
    handle_parsing_errors=True,
    max_iterations=3,      # Prevent infinite loops
)

# ---------------------------------------------------------
# 7️⃣ Test the Agent
print("\n🔎 Example 1: Simple Reasoning Question")
response = agent.invoke({"input": "How many members does the A Team have?"})
print("🤖 Final Answer:", response["output"])

print("\n🔎 Example 2: Math Question")
response = agent.invoke({"input": "What is 100 divided by 25?"})
print("🤖 Final Answer:", response["output"])

# =========================================================
# END OF SCRIPT
# =========================================================
