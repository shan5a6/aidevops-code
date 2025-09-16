from dotenv import load_dotenv, find_dotenv
from langchain_groq import ChatGroq
from langchain.prompts.pipeline import PipelinePromptTemplate
from langchain.prompts import PromptTemplate
from langchain_core.messages import SystemMessage

# 1. Load environment variables (Groq API Key picked automatically)
load_dotenv(find_dotenv())

# 2. Create Introduction Prompt
introduction_template = """
Interpret the text and evaluate the text. 
Determine if the text has a positive, neutral, or negative sentiment. 
Also, identify the subject of the text in one word.
"""
introduction_prompt = PromptTemplate.from_template(introduction_template)

# 3. Create Example Prompt (to guide model thinking - Chain-of-Thought style)
example_template = """
Chain-of-Thought Prompts:
Let's start by evaluating a statement. Consider: "{example_text}". 
How does this make you feel about {example_subject}?
Response: {example_evaluation}

Based on the {example_sentiment} nature of that statement, 
how would you format your response?
Response: {example_format}
"""
example_prompt = PromptTemplate.from_template(example_template)

# 4. Create Execution Prompt (actual input to process)
execution_template = """
Now, execute this process for the text: "{input}".
"""
execution_prompt = PromptTemplate.from_template(execution_template)

# 5. Combine Prompts into a Full Prompt
full_template = """{introduction}

{example}

{execution}"""
full_prompt = PromptTemplate.from_template(full_template)

# 6. Create PipelinePromptTemplate to stitch everything together
input_prompts = [
    ("introduction", introduction_prompt),
    ("example", example_prompt),
    ("execution", execution_prompt)
]
pipeline_prompt = PipelinePromptTemplate(final_prompt=full_prompt, pipeline_prompts=input_prompts)

# 7. Format the Final Prompt with Variables
formatted_prompt = pipeline_prompt.format(
    example_text="The BellaVista restaurant offers an exquisite dining experience. The flavors are rich and the presentation is impeccable.",
    example_subject="BellaVista",
    example_evaluation="It sounds like a positive review for BellaVista.",
    example_sentiment="positive",
    example_format='{ "sentiment": "positive", "subject": "BellaVista" }',
    input="The new restaurant downtown has bland dishes and the wait time is too long."
)

# 8. Initialize Groq LLM
llm = ChatGroq(model_name="llama-3.3-70b-versatile")

# 9. Invoke LLM with the full prompt
result = llm.invoke([SystemMessage(content=formatted_prompt)])

# 10. Print Result
print("\n--- Composed Prompt Result ---")
print(result.content)
