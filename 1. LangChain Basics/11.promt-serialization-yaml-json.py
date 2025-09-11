"""
LangChain Example – Prompt Serialization with Save/Load
We will:
1. Create a PromptTemplate
2. Save it as YAML and JSON
3. Load it back dynamically
4. Send it to Groq LLM
"""

from dotenv import load_dotenv, find_dotenv
from langchain.prompts import PromptTemplate, load_prompt
from langchain_groq import ChatGroq  # Groq LLM

# 1. Load environment variables (make sure GROQ_API_KEY is set in .env)
load_dotenv(find_dotenv())

# 2. Create a PromptTemplate
prompt = PromptTemplate(
    input_variables=["input"],
    template="Tell me a joke about {input}"
)

# 3. Save prompt as YAML and JSON
prompt.save("prompt.yaml")
prompt.save("prompt.json")

# 4. Load prompts back
yaml_prompt = load_prompt("prompt.yaml")
json_prompt = load_prompt("prompt.json")

# 5. Format prompts with dynamic input
yaml_formatted = yaml_prompt.format(input="chickens")
json_formatted = json_prompt.format(input="cows")

print("🟢 Loaded YAML Prompt:", yaml_formatted)
print("🟢 Loaded JSON Prompt:", json_formatted)

# 6. Send formatted prompt to Groq LLM
llm = ChatGroq(model="llama-3.3-70b-versatile")

print("\n🔵 Sending YAML Prompt to Groq...")
yaml_response = llm.invoke(yaml_formatted)
print("💬 Groq Response (YAML):", yaml_response.content)

print("\n🔵 Sending JSON Prompt to Groq...")
json_response = llm.invoke(json_formatted)
print("💬 Groq Response (JSON):", json_response.content)