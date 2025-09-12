"""
LangChain Example – Response Schemas + Structured Output Parser with Groq
"""

from dotenv import load_dotenv, find_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.llm import LLMChain
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

# 1. Load environment variables
load_dotenv(find_dotenv())

# 2. Define response schemas
response_schemas = [
    ResponseSchema(name="sentiment", description="is the text in a positive, neutral or negative sentiment? Sentiment is required."),
    ResponseSchema(name="subject", description="What subject is the text about? Use exactly one word. Use None if no subject was provided."),
    ResponseSchema(name="price", description="How much did the customer pay? Use None if no price was provided.", type="float")
]

# 3. Create a structured output parser
parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = parser.get_format_instructions()
print(format_instructions)

# 4. Define the prompt template (include format instructions!)
TEMPLATE = """
Analyze the following review and extract structured data.

{format_instructions}

Review text:
{input}
"""

prompt_template = ChatPromptTemplate.from_template(
    TEMPLATE, partial_variables={"format_instructions": format_instructions}
)

# 5. Initialize Groq LLM
llm = ChatGroq(model="llama-3.3-70b-versatile")

# 6. Create the chain
chain = LLMChain(llm=llm, prompt=prompt_template)

# 7. Run the chain
raw_result = chain.invoke(input="I paid 20 dollars for a burger. It was too salty and not worth the price!")
print("\n📝 Raw Model Output:")
print(raw_result)

# 8. Parse the output into structured data
parsed_result = parser.parse(raw_result['text'])
print("\n✅ Parsed Python Dictionary:")
print(parsed_result)
