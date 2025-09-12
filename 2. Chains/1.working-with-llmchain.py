"""
LangChain Example – Using LLMChain with Groq
We will:
1. Create a structured prompt
2. Combine it with Groq LLM using LLMChain
3. Get structured JSON output
"""

from dotenv import load_dotenv, find_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.llm import LLMChain

# 1. Load environment variables
load_dotenv(find_dotenv())

# 2. Define Prompt Template
TEMPLATE = """
Interprete the text and evaluate the text.
sentiment: is the text in a positive, neutral or negative sentiment? Sentiment is required.
subject: What subject is the text about? Use exactly one word. Use 'None' if no subject was provided.
price: How much did the customer pay? Use 'None' if no price was provided.

Format the output as JSON with the following keys:
sentiment
subject
price

text: {input}
"""

# 3. Convert Template into ChatPromptTemplate
prompt_template = ChatPromptTemplate.from_template(template=TEMPLATE)

# 4. Initialize Groq LLM
llm = ChatGroq(model="llama-3.3-70b-versatile")

# 5. Create LLMChain
chain = LLMChain(llm=llm, prompt=prompt_template)

# 6. Call the chain with sample input
result = chain.invoke(input="I ordered pizza salami from the restaurant Bellavista. It was ok, but the dough could have been a bit more crisp.")
print("\n🔎 Structured Output from Groq:")
print(result)
