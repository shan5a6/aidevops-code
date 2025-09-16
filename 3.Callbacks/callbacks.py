from dotenv import load_dotenv, find_dotenv
from langchain.callbacks import StdOutCallbackHandler
from langchain_community.callbacks.manager import get_openai_callback
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq

# 1. Load environment variables (including GROQ_API_KEY)
load_dotenv(find_dotenv())

# 2. Instantiate Groq LLM
llm = ChatGroq(model="llama-3.3-70b-versatile")

# 3. Prompt Template
prompt_template = PromptTemplate(
    input_variables=["input"],
    template="Tell me a joke about {input}"
)
chain = LLMChain(llm=llm, prompt=prompt_template)

# 4. StdOut Callback Handler
handler = StdOutCallbackHandler()
config = {'callbacks': [handler]}
chain.invoke(input="rabbit", config=config)

# 5. Custom Callback Handler
class MyCustomHandler(BaseCallbackHandler):
    def on_llm_end(self, response, **kwargs) -> None:
        print(f"RESPONSE: {response}")

handler = MyCustomHandler()
config = {'callbacks': [handler]}
chain.invoke(input="rabbit", config=config)

# 6. Context manager to track token usage and cost
with get_openai_callback() as cb:
    chain.invoke(input="rabbit")

print(f"Total Cost: {cb.total_cost}")
