from dotenv import load_dotenv, find_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

# 1. Load environment variables (GROQ_API_KEY)
load_dotenv(find_dotenv())

# 2. Initialize Groq LLM
llm = ChatGroq(
    model_name="llama-3.3-70b-versatile"
)

# 3. Prepare batch conversations
batch_messages = [
    [
        SystemMessage(content="You are a helpful assistant that translates English to German"),
        HumanMessage(content="Do you have vegan options?")
    ],
    [
        SystemMessage(content="You are a helpful assistant that translates English to Spanish"),
        HumanMessage(content="Do you have vegan options?")
    ],
]

# 4. Send batch to LLM
batch_result = llm.generate(batch_messages)

# 5. Extract translations
translations = [generation[0].message.content for generation in batch_result.generations]
print(translations)
# 6. Print translations
for i, t in enumerate(translations, 1):
    print(f"Translation {i}:", t)
