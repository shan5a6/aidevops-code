# 1. Load environment variables safely
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())  # Looks for .env file and loads API keys

# 2. Import Groq LLM from LangChain
from langchain_groq import ChatGroq

# 3. Initialize the LLM
llm = ChatGroq(
    model_name="llama-3.3-70b-versatile"      # Enterprise-grade Groq model
)

# 4. Send prompts to the model
response1 = llm.invoke("Tell me a joke about developers")
print("Joke 1:", response1.content)

response2 = llm.invoke("Tell me another joke about DevOps")
print("Joke 2:", response2.content)

# 5. Enterprise Example
response3 = llm.invoke("Summarize this meeting: We discussed migrating AWS to Azure for cost savings.")
print("Enterprise Summary:", response3.content)


