from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
import os

os.environ["GROQ_API_KEY"] = "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"

chat_model = ChatGroq(
    model="llama3-70b-8192",
    temperature=0.7, 
    max_tokens=500,
    api_key=os.environ["GROQ_API_KEY"]
)

class Movie(BaseModel):
    title: str = Field(description="The title of the movie.")
    genre: list[str] = Field(description="The genre of the movie.")
    year: int = Field(description="The year the movie was released.")

parser = PydanticOutputParser(pydantic_object=Movie)

prompt_template_text = """
Response with a movie recommendation based on the query:\n
{format_instructions}\n
{query}
"""

format_instructions = parser.get_format_instructions()

prompt_template = PromptTemplate(
    template=prompt_template_text,
    input_variables=["query"],
    partial_variables={"format_instructions": format_instructions},
)

prompt = prompt_template.format(query="A 90s movie with Nicolas Cage.")

text_output = chat_model.invoke(prompt)

print("Raw Output:")
print(text_output.content)
parsed_output = parser.parse(text_output.content)

print("\nParsed Output:")
print(parsed_output)  
