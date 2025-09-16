"""
LangChain - Few-Shot Prompting with Groq
--------------------------------------
This script demonstrates how to use FewShotPromptTemplate in LangChain
to classify customer reviews with sentiment and subject detection.
"""

from dotenv import load_dotenv, find_dotenv
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage

# 1. Load environment variables (GROQ_API_KEY)
load_dotenv(find_dotenv())

# 2. Define few-shot examples
examples = [
    {
        "text": "The BellaVista restaurant offers an exquisite dining experience. The flavors are rich and the presentation is impeccable.",
        "response": "sentiment: positive\nsubject: BellaVista"
    },
    {
        "text": "BellaVista restaurant was alright. The food was decent, but nothing stood out.",
        "response": "sentiment: neutral\nsubject: BellaVista"
    },
    {
        "text": "I was disappointed with BellaVista. The service was slow and the dishes lacked flavor.",
        "response": "sentiment: negative\nsubject: BellaVista"
    },
    {
        "text": "SeoulSavor offered the most authentic Korean flavors I've tasted outside of Seoul. The kimchi was perfectly fermented and spicy.",
        "response": "sentiment: positive\nsubject: SeoulSavor"
    }
]

# 3. Add more examples dynamically if needed
new_example = {
    "text": "SeoulSavor was okay. The bibimbap was good but the bulgogi was a bit too sweet for my taste.",
    "response": "sentiment: neutral\nsubject: SeoulSavor"
}
examples.append(new_example)

# 4. Define example prompt format
example_prompt = PromptTemplate(
    input_variables=["text", "response"],
    template="Text: {text}\n{response}"
)

# 5. Create FewShotPromptTemplate
prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    suffix="text: {input}",
    input_variables=["input"]
)

# 6. Format prompt with new user input
user_review = "The MunichDeals experience was just awesome!"
formatted_prompt = prompt.format(input=user_review)

# 7. Initialize Groq LLM
llm = ChatGroq(model_name="llama-3.3-70b-versatile")

# 8. Send prompt to LLM as a system message
system_msg = SystemMessage(content=formatted_prompt)
result = llm.invoke([system_msg])

# 9. Print output
print("🔎 User Review:", user_review)
print("🤖 AI Analysis:\n", result.content)
