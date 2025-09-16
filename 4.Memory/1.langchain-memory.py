from dotenv import load_dotenv, find_dotenv

# 1. Load environment variables (like GROQ_API_KEY)
load_dotenv(find_dotenv())

# 2. Import Memory utilities
from langchain.memory import ChatMessageHistory, ConversationBufferMemory

# 3. Create basic chat history
history = ChatMessageHistory()
history.add_user_message("hi!")  # User says hi
history.add_ai_message("hello my friend!")  # AI responds

print("History Messages:", history.messages)
# Output: You will see both user and AI messages stored

# 4. Using ConversationBufferMemory to maintain state
memory = ConversationBufferMemory()
memory.chat_memory.add_user_message("hi!")
memory.chat_memory.add_ai_message("hello my friend!")

print("Memory Variables:", memory.load_memory_variables({}))
# Output: Shows {"history": "User: hi!\nAI: hello my friend!"}

# 5. Connecting Memory with a ConversationChain using Groq
from langchain_groq import ChatGroq
from langchain.chains.conversation.base import ConversationChain

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

conversation = ConversationChain(
    llm=llm, 
    verbose=True, 
    memory=ConversationBufferMemory()
)

# First message
response1 = conversation.invoke(input="What is the capital of France?")
print("AI Response 1:", response1)

# Second message - this uses memory (it knows we asked about France)
response2 = conversation.invoke(input="Whats the best food there?")
print("AI Response 2:", response2)
