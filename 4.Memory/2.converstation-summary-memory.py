from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())  # Load GROQ_API_KEY from .env file

# 1. Import the required memory and chain classes
from langchain.memory import ConversationSummaryBufferMemory
from langchain.chains import ConversationChain
from langchain_groq import ChatGroq

# 2. Initialize Groq LLM
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# 3. Sample review text (long input)
review = """I ordered Pizza Salami for 9.99$ and it was awesome!
The pizza was delivered on time and was still hot when I received it.
The crust was thin and crispy, and the toppings were fresh and flavorful.
The Salami was well-cooked and complemented the cheese perfectly.
The price was reasonable and I believe I got my money's worth.
Overall, I am very satisfied with my order and I would recommend this pizza place to others."""

# 4. Create ConversationSummaryBufferMemory
# max_token_limit=100 means we will summarize as soon as history exceeds ~100 tokens.
summary_memory = ConversationSummaryBufferMemory(llm=llm, max_token_limit=100)

# 5. Simulate storing conversation context
summary_memory.save_context(
    {"input": "Hello, how can I help you today?"},
    {"output": "Could you analyze a review for me?"},
)

summary_memory.save_context(
    {"input": "Sure, I'd be happy to. Could you provide the review?"},
    {"output": f"{review}"},
)

# 6. Connect memory with a ConversationChain
conversation = ConversationChain(
    llm=llm,
    verbose=True,
    memory=summary_memory
)

# 7. Invoke conversation with a follow-up
response = conversation.invoke(input="Thank you very much!")
print("AI Response:", response)

# 8. Check what memory looks like now (you'll see the summary)
print("Memory Variables:", summary_memory.load_memory_variables({}))
