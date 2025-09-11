from dotenv import load_dotenv, find_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# 1. Load environment variables
load_dotenv(find_dotenv())

# 2. Initialize Groq LLM
llm = ChatGroq(
    model_name="llama-3.3-70b-versatile"
)

#3. Single-turn example
single_result = llm.invoke("Tell me a joke about cows")
print("Single-turn joke:", single_result.content)

# 4. Multi-turn conversation
messages = [
    SystemMessage(content="You are a helpful assistant specialized in providing information about BellaVista Italian Restaurant."),
    HumanMessage(content="What's on the menu?"),
    AIMessage(content="BellaVista offers a variety of Italian dishes including pasta, pizza, and seafood."),
    HumanMessage(content="Do you have vegan options?")
]

conversation_result = llm.invoke(input=messages)
print("Multi-turn response:", conversation_result.content)
