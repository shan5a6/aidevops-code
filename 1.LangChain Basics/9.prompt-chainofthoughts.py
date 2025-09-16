from dotenv import load_dotenv, find_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain_core.messages import SystemMessage

# 1. Load environment variables (Groq API key will be read automatically)
load_dotenv(find_dotenv())

# 2. Define Chain-of-Thought Template (escaped braces for JSON output)
TEMPLATE = """
Interpret the text and evaluate the text. 
Determine if the text has a positive, neutral, or negative sentiment. 
Also, identify the subject of the text in one word.

Format the output as JSON with the following keys:
sentiment
subject

text: {input}

Chain-of-Thought Prompts:
Let's start by evaluating a statement. Consider: "The BellaVista restaurant offers an exquisite dining experience. The flavors are rich and the presentation is impeccable." How does this make you feel about BellaVista?
 It sounds like a positive review for BellaVista.

Based on the positive nature of that statement, how would you format your response?
 {{ "sentiment": "positive", "subject": "BellaVista" }}

Now, think about this: "SeoulSavor was okay. The bibimbap was good but the bulgogi was a bit too sweet for my taste." Does this give a strong feeling either way?
 Not particularly. It seems like a mix of good and not-so-good elements, so it's neutral.

Given the neutral sentiment, how should this be presented?
 {{ "sentiment": "neutral", "subject": "SeoulSavor" }}

Lastly, ponder on this: "I was let down by MunichMeals. The potato salad lacked flavor and the staff seemed uninterested." What's the overall impression here?
 The statement is expressing disappointment and dissatisfaction.

And if you were to categorize this impression, what would it be?
 {{ "sentiment": "negative", "subject": "MunichMeals" }}
"""

# 3. Create PromptTemplate
prompt_template = PromptTemplate(template=TEMPLATE, input_variables=["input"])

# 4. Format prompt with input text
formatted_prompt = prompt_template.format(
    input="The MunichDeals experience was just awesome!"
)

# 5. Initialize Groq LLM
llm = ChatGroq(model_name="llama-3.3-70b-versatile")

# 6. Invoke the model
result = llm.invoke([SystemMessage(content=formatted_prompt)])

# 7. Print the result
print("\n--- Chain-of-Thought Result ---")
print(result.content)
