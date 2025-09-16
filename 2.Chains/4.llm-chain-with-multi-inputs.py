from dotenv import load_dotenv, find_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.llm import LLMChain

# Load environment variables
load_dotenv(find_dotenv())

# 1. Instantiate Groq LLM
llm = ChatGroq(model="llama-3.3-70b-versatile")

# 2. Single-input chain
prompt_template = PromptTemplate(input_variables=["input"], template="Tell me a joke about {input}")
chain = LLMChain(llm=llm, prompt=prompt_template)
print("Single Input Output:")
print(chain.invoke(input="a parrot"))

# 3. Multi-input chain
prompt_template = PromptTemplate(input_variables=["input", "language"], template="Tell me a joke about {input} in {language}")
chain = LLMChain(llm=llm, prompt=prompt_template)
print("\nMulti Input Output:")
print(chain.invoke({"input": "a parrot", "language": "german"}))
