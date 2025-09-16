from dotenv import load_dotenv, find_dotenv
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.llm import LLMChain
from langchain.chains.router import MultiPromptChain
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from langchain.chains.router.multi_prompt_prompt import MULTI_PROMPT_ROUTER_TEMPLATE

# 1. Load env
load_dotenv(find_dotenv())

# 2. Instantiate Groq LLM
llm = ChatGroq(model="llama-3.3-70b-versatile")

# 3. Define templates
positive_template = """You are an AI that focuses on the positive side. Highlight positive aspects. {input}"""
neutral_template = """You are an AI with a neutral perspective. Provide balanced analysis. {input}"""
negative_template = """You are an AI designed to find negative aspects. Analyze downsides. {input}"""

prompt_infos = [
    {"name": "positive", "description": "Good for positive sentiments", "prompt_template": positive_template},
    {"name": "neutral", "description": "Good for neutral sentiments", "prompt_template": neutral_template},
    {"name": "negative", "description": "Good for negative sentiments", "prompt_template": negative_template},
]

# 4. Create destination chains
destination_chains = {}
for p_info in prompt_infos:
    prompt = PromptTemplate(template=p_info["prompt_template"], input_variables=["input"])
    destination_chains[p_info["name"]] = LLMChain(llm=llm, prompt=prompt)

# 5. Create router chain
destinations_str = "\n".join([f"{p['name']}: {p['description']}" for p in prompt_infos])
router_prompt = PromptTemplate(
    template=MULTI_PROMPT_ROUTER_TEMPLATE.format(destinations=destinations_str),
    input_variables=["input"],
    output_parser=RouterOutputParser(),
)
router_chain = LLMRouterChain.from_llm(llm, router_prompt)

# 6. Create MultiPromptChain
multi_chain = MultiPromptChain(
    router_chain=router_chain,
    destination_chains=destination_chains,
    default_chain=destination_chains["neutral"],
    verbose=True
)

# 7. Invoke chain
result = multi_chain.invoke({"input": "I ordered Pizza Salami for 9.99$ and it was awesome!"})
print(result)
