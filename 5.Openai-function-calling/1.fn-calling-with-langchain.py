"""
LangChain Function Calling (Tool Calling) Example with Groq LLM
"""

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())  # ✅ Loads GROQ_API_KEY from .env file

from langchain_groq import ChatGroq  # ✅ Using Groq instead of OpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage

# 1️⃣ Create the LLM
llm = ChatGroq(model="llama-3.3-70b-versatile")

# ✅ First, just invoke the LLM directly
print(llm.invoke("How will the weather be in Munich today?").content)


# 2️⃣ Define Tools (Functions that the LLM can call)
@tool
def fake_weather_api(city: str) -> str:
    """
    Check the weather in a specified city.
    """
    return f"The weather in {city} is Sunny, 22°C"


@tool
def outdoor_seating_availability(city: str) -> str:
    """
    Check if outdoor seating is available at a specified restaurant in a given city.
    """
    return f"Yes, outdoor seating is available in {city}."


# 3️⃣ Bind the tools to the LLM
tools = [fake_weather_api, outdoor_seating_availability]
llm_with_tools = llm.bind_tools(tools)

# 4️⃣ Let the LLM decide which tools to call
print("\n--- First Query ---")
result = llm_with_tools.invoke("How will the weather be in Munich today?")
print(result)

print("\n--- Second Query with Multiple Needs ---")
result = llm_with_tools.invoke(
    "How will the weather be in Munich today? Do you still have seats outdoor available?"
)
print(result)

# 5️⃣ Manual Tool Invocation Flow (More Control)
messages = [
    HumanMessage("How will the weather be in Munich today? I would like to eat outside if possible")
]

# Get LLM's response (it may request a tool call)
llm_output = llm_with_tools.invoke(messages)
messages.append(llm_output)

# Map tool calls to actual Python functions
tool_mapping = {
    "fake_weather_api": fake_weather_api,
    "outdoor_seating_availability": outdoor_seating_availability,
}

for tool_call in llm_output.tool_calls:
    tool = tool_mapping[tool_call["name"]]
    tool_output = tool.invoke(tool_call["args"])
    messages.append(ToolMessage(tool_output, tool_call_id=tool_call["id"]))

# Get final LLM response after tool execution
final_response = llm_with_tools.invoke(messages)
print("\n--- Final Answer After Tool Calls ---")
print(final_response)
