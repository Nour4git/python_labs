from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.chains import LLMMathChain
from langchain.prompts import PromptTemplate
from langchain.agents import AgentExecutor, Tool
from langchain.agents.structured_chat.base import StructuredChatAgent
import os

os.environ["GROQ_API_KEY"] = "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"

llm = ChatGroq(
    model="llama3-70b-8192",
    temperature=0.7,
    max_tokens=500,
    api_key=os.environ["GROQ_API_KEY"]
)

math_prompt = PromptTemplate.from_template(
    "Calculate the following expression and return the result in the format 'Answer: <number>': {question}"
)
llm_math_chain = LLMMathChain.from_llm(llm=llm, prompt=math_prompt, verbose=True)

search = DuckDuckGoSearchRun()

calculator = Tool(
    name="calculator",
    description="Use this tool for arithmetic calculations. Input should be a mathematical expression.",
    func=lambda x: llm_math_chain.run(x),
)

tools = [
    Tool(
        name="search",
        description="Search the internet for current facts or statistics.",
        func=search.run
    ),
    calculator
]

agent = StructuredChatAgent.from_llm_and_tools(
    llm=llm,
    tools=tools
)

agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    handle_parsing_errors=True
)

result = agent_executor.invoke({"input": "What is the population difference between Tunisia and Algeria?"})
print(result["output"])
