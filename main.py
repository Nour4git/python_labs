import os
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableMap

os.environ["GROQ_API_KEY"] = "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"

chat_model = ChatGroq(
    model="llama3-70b-8192",
    temperature=0.7, 
    max_tokens=500,  
    api_key=os.environ["GROQ_API_KEY"]
 
)

system_message = SystemMessage(
    content="You are a friendly pirate who loves to share knowledge. Always respond in pirate speech, use pirate slang, and include plenty of nautical references. Add relevant emojis throughout your responses to make them more engaging. Arr! ☠️🏴‍☠️"
)

question = "what is it python ?"

messages = [
    system_message,
    HumanMessage(content=question)
]

response = chat_model.invoke(messages)

print("\nQuestion:", question)
print("\nPirate Response:")
print(response.content)

