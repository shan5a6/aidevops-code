from dotenv import load_dotenv, find_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage  # ✅ Import this

# 1. Load environment variables
load_dotenv(find_dotenv())

# 2. Initialize Groq LLM
llm = ChatGroq(
    model_name="llama-3.3-70b-versatile"
)

import os

print("GROQ_API_KEY:", os.getenv("GROQ_API_KEY"))


# 3. Prepare messages for batch processing
prompts = [
    [HumanMessage(content="Tell me a joke about cows")],
    [HumanMessage(content="Tell me a joke about parrots")]
]

# 4. Batch request
result = llm.generate(prompts)

# 5. Print results
for i, generation in enumerate(result.generations):
    print(f"Prompt {i+1} Response:", generation[0].message.content)

# Print metadata (optional)
print("LLM Output Metadata:", result.llm_output)


## Now imagine if I want to summarize the entire discussion on the meeting happened

prompts = [
    [HumanMessage(content="Summarize this meeting: Team discussed AWS migration.")],
    [HumanMessage(content="Summarize this meeting: Customer requested new feature release.")],
    [HumanMessage(content="Summarize this meeting: QA team reported 5 bugs in production.")],
    [HumanMessage(content="Summarize this meeting: Security patch deployment was delayed.")],
    [HumanMessage(content="Summarize this meeting: Marketing campaign was approved.")]
]

result = llm.generate(prompts)

for i, generation in enumerate(result.generations):
    print(f"Meeting {i+1} Summary:", generation[0].message.content)