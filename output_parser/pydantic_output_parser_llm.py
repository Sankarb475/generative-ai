# app_pydantic_parser.py

import os
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, ValidationError
from typing import Optional, List


# 1. Define your Pydantic Model for the desired output structure
class PersonInfo(BaseModel):
    """Information about a person."""
    name: str = Field(description="The full name of the person")
    age: Optional[int] = Field(description="The age of the person, if known", default=None)
    occupation: Optional[str] = Field(description="The person's occupation", default=None)
    hobbies: List[str] = Field(description="A list of hobbies the person enjoys", default_factory=list)
    is_fictional: bool = Field(description="True if the person is fictional, False otherwise")



def run_pydantic_parser_example():
    """
    Demonstrates using a PydanticOutputParser with a local Ollama Llama2 model.
    """
    # Initialize the LLM (Ollama with Llama2)
    # Ensure Ollama is installed and running, and the 'llama2' model is downloaded.
    # Run 'ollama run llama2' in a separate terminal before executing this script.
    try:
        llm = Ollama(model="llama2")
    except Exception as e:
        print(f"Error initializing Ollama LLM. Make sure Ollama is installed, running,")
        print(f"and the 'llama2' model is downloaded (e.g., by running 'ollama run llama2').")
        print(f"Error details: {e}")
        return

  
    # 2. Create an instance of the PydanticOutputParser
    # This parser will generate instructions for the LLM based on your Pydantic model.
    parser = PydanticOutputParser(pydantic_object=PersonInfo)

  
    # 3. Define the prompt template
    # IMPORTANT: Include the parser's format instructions in your prompt.
    # This tells the LLM how to format its output so the parser can understand it.
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert at extracting structured information from text."),
        ("user", "Extract information about the following person:\n\n{text}\n\n{format_instructions}"),
    ]).partial(format_instructions=parser.get_format_instructions()) # Inject format instructions

  
    # 4. Create the chain
    chain = prompt | llm | parser

  
    # 5. Invoke the chain with some text about a person
    text_about_person = "My name is Alice, and I am 30 years old. I work as a software engineer and love hiking, reading, and coding. I am a real person."
    print(f"Input Text:\n{text_about_person}\n")

  
    try:
        # The chain will now return a PersonInfo object
        person_info: PersonInfo = chain.invoke({"text": text_about_person})

        print("--- Extracted Person Info (Pydantic Object) ---")
        print(f"Name: {person_info.name}")
        print(f"Age: {person_info.age}")
        print(f"Occupation: {person_info.occupation}")
        print(f"Hobbies: {', '.join(person_info.hobbies)}")
        print(f"Is Fictional: {person_info.is_fictional}")
        print(f"Raw Pydantic Object: {person_info.model_dump()}") # Convert back to dict for inspection

    except ValidationError as e:
        print(f"Validation Error: The LLM output did not match the Pydantic schema.")
        print(f"Error details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

  
    print("\n--- Another Example (Fictional Character) ---")
    text_about_fictional = "Meet Sherlock Holmes, a brilliant detective known for his deductive reasoning. He enjoys playing the violin and solving mysteries. He is a character from books."
    print(f"Input Text:\n{text_about_fictional}\n")

  
    try:
        person_info_fictional: PersonInfo = chain.invoke({"text": text_about_fictional})
        print("--- Extracted Fictional Person Info ---")
        print(f"Name: {person_info_fictional.name}")
        print(f"Age: {person_info_fictional.age}") # Will be None if LLM doesn't infer
        print(f"Occupation: {person_info_fictional.occupation}")
        print(f"Hobbies: {', '.join(person_info_fictional.hobbies)}")
        print(f"Is Fictional: {person_info_fictional.is_fictional}")

    except ValidationError as e:
        print(f"Validation Error for fictional character: {e}")
      
    except Exception as e:
        print(f"An unexpected error occurred for fictional character: {e}")


if __name__ == "__main__":
    run_pydantic_parser_example()






# output 
{
"description": "Information about a person.",
"properties": {
"name": {
"title": "Name",
"type": "string"
},
"age": {
"anyOf": [
{
"type": "integer"
},
{
"type": "null"
}
],
"default": null,
"description": "The age of the person, if known",
"title": "Age"
},
"occupation": {
"anyOf": [
{
"type": "string"
},
{
"type": "null"
}
],
"default": null,
"description": "The person's occupation",
"title": "Occupation"
},
"hobbies": {
"items": {
"type": "string"
},
"title": "Hobbies",
"type": "array"
},
"is_fictional": {
"description": "True if the person is fictional, False otherwise",
"title": "Is Fictional",
"type": "boolean"
},
"required": [
"name",
"is_fictional"
]
}
}
