import os
from dotenv import load_dotenv, find_dotenv

# Loading environment variables
load_dotenv(find_dotenv())

# First way
from langchain.chat_models import init_chat_model
model = init_chat_model("llama-3.3-70b-versatile", model_provider="groq")
print(model.invoke("Hello, world!").content)


# 2nd way
from langchain_groq import ChatGroq

llm = ChatGroq(model_name="llama-3.3-70b-versatile")
response = llm.invoke("Hello, how are you?")
print(response)

# Like wise if you want to call other models then its same .. 

from langchain_openai import OpenAI

llm = OpenAI(
    model="gpt-3.5-turbo-instruct",
    api_key="your_openai_api_key"
)

print(llm.invoke("Write a Python hello world program"))