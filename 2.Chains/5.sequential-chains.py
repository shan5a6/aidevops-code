from dotenv import load_dotenv, find_dotenv
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.llm import LLMChain
from langchain.chains.sequential import SequentialChain

# 1. Load environment variables
load_dotenv(find_dotenv())

# 2. Instantiate Groq LLM
llm = ChatGroq(model="llama-3.3-70b-versatile")

# 3. Define all LLMChains
prompt_review = PromptTemplate.from_template(
    template="You ordered {dish_name} and your experience was {experience}. Write a review: "
)
chain_review = LLMChain(llm=llm, prompt=prompt_review, output_key="review")

prompt_comment = PromptTemplate.from_template(
    template="Given the restaurant review: {review}, write a follow-up comment: "
)
chain_comment = LLMChain(llm=llm, prompt=prompt_comment, output_key="comment")

prompt_summary = PromptTemplate.from_template(
    template="Summarise the review in one short sentence: \n\n {comment}"
)
chain_summary = LLMChain(llm=llm, prompt=prompt_summary, output_key="summary")

prompt_translation = PromptTemplate.from_template(
    template="Translate the summary to german: \n\n {summary}"
)
chain_translation = LLMChain(llm=llm, prompt=prompt_translation, output_key="german_translation")

# 4. Create SequentialChain
overall_chain = SequentialChain(
    chains=[chain_review, chain_comment, chain_summary, chain_translation],
    input_variables=["dish_name", "experience"],
    output_variables=["review", "comment", "summary", "german_translation"],
)

# 5. Run the chain
result = overall_chain.invoke({"dish_name": "Pizza Salami", "experience": "It was awful!"})
print(result)
