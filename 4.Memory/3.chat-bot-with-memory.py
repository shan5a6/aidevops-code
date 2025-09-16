"""Interactive Streamlit Chatbot with Summarizing Memory (Groq)"""

import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv, find_dotenv
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationSummaryBufferMemory
from langchain_community.chat_message_histories.streamlit import (
    StreamlitChatMessageHistory,
)
from langchain.globals import get_verbose

# 🔑 Load environment variables (for GROQ_API_KEY)
load_dotenv(find_dotenv())

# 📢 Optional verbose logging (prints detailed execution)
get_verbose()

# 🎨 Streamlit Page Config
st.set_page_config(page_title="LangChain Memory Chatbot", page_icon=":robot_face:")
st.title("🤖 LangChain Chatbot with Smart Memory")
st.markdown(
    "This chatbot remembers your conversation and **summarizes old messages** to keep responses relevant, "
    "even in long chats. Perfect for enterprise-grade AI assistants!"
)

# --- 🛠️ Configurable Parameters ---
with st.sidebar:
    st.header("⚙️ Model Configuration")
    temperature = st.slider("Creativity (Temperature)", 0.0, 1.0, 0.2, 0.1)
    max_tokens = st.slider("Max Tokens per Summary", 50, 500, 150, 50)

# 📝 Prompt Template
template = """You are a helpful AI assistant having a conversation with a human.

{history}
Human: {human_input}
AI:"""
prompt = PromptTemplate(input_variables=["history", "human_input"], template=template)

# 💬 Chat history object
msgs = StreamlitChatMessageHistory(key="special_app_key")

# 🧠 Summary Memory (Automatically summarizes when token count exceeds max_tokens)
memory = ConversationSummaryBufferMemory(
    llm=ChatGroq(model="llama-3.3-70b-versatile", temperature=temperature),
    memory_key="history",
    chat_memory=msgs,
    max_token_limit=max_tokens
)

# 🔗 Load LLM chain
def load_chain():
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=temperature)
    return LLMChain(llm=llm, prompt=prompt, memory=memory)

# 🧱 Initialize Streamlit session state
def initialize_session_state():
    if "chain" not in st.session_state:
        st.session_state.chain = load_chain()
    if "generated" not in st.session_state:
        st.session_state.generated = []
    if "past" not in st.session_state:
        st.session_state.past = []
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""
    if "widget_input" not in st.session_state:
        st.session_state.widget_input = ""

initialize_session_state()

# 📥 Capture user input
def submit():
    st.session_state.user_input = st.session_state.widget_input
    st.session_state.widget_input = ""

st.text_input("💬 Your Message:", key="widget_input", on_change=submit)

# 🤖 Generate response
if st.session_state.user_input:
    output = st.session_state.chain.invoke(st.session_state.user_input)["text"]
    st.session_state.past.append(st.session_state.user_input)
    st.session_state.generated.append(output)
    st.session_state.user_input = ""

# 💬 Display chat history
if st.session_state["generated"]:
    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")

# 🔎 Show memory summary (for learning/demo)
with st.expander("🧠 Show Current Memory State"):
    memory_state = memory.load_memory_variables({})
    st.json(memory_state)
