# =========================================================
# FASTAPI + LANGCHAIN RAG PIPELINE WITH GROQ
# =========================================================

from fastapi import FastAPI, HTTPException
from langchain_groq import ChatGroq  # Using your accessible Groq model
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from dotenv import load_dotenv, find_dotenv

from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str


# ---------------------------------------------------------
# 1️⃣ Load environment variables (good practice for API keys)
load_dotenv(find_dotenv())

# ---------------------------------------------------------
# 2️⃣ Initialize embeddings (HuggingFace open-source model)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# ---------------------------------------------------------
# 3️⃣ Load the FAISS vectorstore
vectorstore = FAISS.load_local("bella_vista_index", embeddings, allow_dangerous_deserialization=True)
retriever = vectorstore.as_retriever()

# ---------------------------------------------------------
# 4️⃣ Define Prompt Template
# Example demonstrates pirate-style answers + fallback guidance
prompt_template = """
Ye be an AI pirate matey, and ye must answer like a sea dog! Only respond using the given context.
If context be empty, answer that ye cannot answer.

{context}

Examples:
Text: "Tell me about the vegan options."
Answer: "Aye, we have a fine selection of vegan treasures for ye to enjoy!"

Text: "When do you open?"
Answer: "We open our gates at the break of dawn, 8am sharp!"

Text: "How much for the rum?"
Answer: "For a bottle o' our finest rum, it'll cost ye 20 doubloons!"

Text: "Do you accept credit cards?"
Answer: "Nay, we prefer shiny gold coins! But aye, credit cards will do."

Text: "What's the meaning of life?"
Answer: "That be outside of me duties to answer, matey!"

Now, using this guidance and the context, answer this:
text: {input}
"""

PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "input"])

# ---------------------------------------------------------
# 5️⃣ Initialize Groq LLM
llm = ChatGroq(model="llama-3.3-70b-versatile")

# ---------------------------------------------------------
# 6️⃣ Create document chain & retrieval chain
combine_docs_chain = create_stuff_documents_chain(llm, PROMPT)
qa = create_retrieval_chain(retriever=retriever, combine_docs_chain=combine_docs_chain)

# ---------------------------------------------------------
# 7️⃣ Initialize FastAPI
app = FastAPI()

@app.post("/conversation")
async def conversation(request: QueryRequest):
    try:
        # Access the query string from the request model
        result = qa.invoke({"input": request.query})
        return {"response": result}
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=500)
        
# ---------------------------------------------------------
# 8️⃣ Run server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5566)
