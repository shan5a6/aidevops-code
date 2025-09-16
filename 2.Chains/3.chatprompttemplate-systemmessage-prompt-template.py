from dotenv import load_dotenv, find_dotenv
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate
from langchain_groq import ChatGroq
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

# 4. Create ChatPromptTemplate with SystemMessage
prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(
            "Interprete the text and evaluate the text. "
            "sentiment: is the text in a positive, neutral or negative sentiment? "
            "subject: What subject is the text about? Use exactly one word. "
            "Just return the JSON, do not add ANYTHING, NO INTERPRETATION! "
            "text: {input}\n"
            "{format_instructions}\n"
        )
    ],
    input_variables=["input"],
    partial_variables={"format_instructions": format_instructions}
)

# 5. Instantiate Groq LLM
llm = ChatGroq(model="llama-3.3-70b-versatile")

# 6. Format the prompt
_input = prompt.format_prompt(
    input="I ordered pizza salami from the restaurant Bellavista. It was ok, but the dough could have been a bit more crisp."
)

# 7. Invoke the model
output = llm.invoke(_input.to_messages())
print("\n📝 Raw Model Output:")
print(output.content)

# 8. Parse the result
json_output = parser.parse(output.content)
print("\n✅ Parsed Python Dictionary:")
print(json_output)

# 9. Access individual fields
print("\n🎯 Sentiment Value Only:")
print(json_output.get("sentiment"))
