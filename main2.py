from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
import os
from langchain.schema import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableMap

os.environ["GROQ_API_KEY"] = "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"

chat_model = ChatGroq(
    model="llama3-70b-8192",
    temperature=0.7, 
    max_tokens=500,
    api_key=os.environ["GROQ_API_KEY"]
)

prompt_template = PromptTemplate.from_template(
    "List {n} cooking/meal titles for {cuisine} cuisine (name only)."
)

chain = prompt_template | chat_model

response = chain.invoke({
    "n": 5,
    "cuisine": "Italian"
})

print("\nPrompt: List 5 cooking/meal titles for Italian cuisine (name only).")
print("\nResponse:")
print(response.content)
