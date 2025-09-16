from dotenv import load_dotenv, find_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

# 1. Load environment variables
load_dotenv(find_dotenv())

# 2. Create dynamic template
TEMPLATE = """
You are a helpful assistant that translates the {input_language} to {output_language}
"""

prompt_template = PromptTemplate(
    template=TEMPLATE,
    input_variables=["input_language", "output_language"]
)

# 3. Fill prompt dynamically
filled_prompt = prompt_template.format(input_language="english", output_language="german")

# 4. Initialize Groq LLM
llm = ChatGroq(model_name="llama-3.3-70b-versatile")

# 5. Create conversation messages
system_msg = SystemMessage(content=filled_prompt)
user_msg = HumanMessage(content="Do you have vegan options?")

# 6. Send conversation to LLM
result = llm.invoke(input=[system_msg, user_msg])

# 7. Print AI response
print("AI Response:", result.content)
