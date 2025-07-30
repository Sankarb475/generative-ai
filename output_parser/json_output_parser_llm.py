import os
# from langchain_openai import ChatOpenAI # For OpenAI models - commented out as we are using Ollama
from langchain_community.llms import Ollama # For local Ollama models
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers import CommaSeparatedListOutputParser,JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field


class CapitalInfo(BaseModel):
    capital: str = Field(description="The capital city of the given country")
    country: str = Field(description="The country for which the capital is being asked")

def run_basic_llm_example():

    # Initialize the LLM
    # Ensure Ollama is installed and running, and the 'llama2' model is downloaded.
    # You can start Ollama and download the model by running:
    # ollama run llama2
    try:
        llm = Ollama(model="llama2")
    except Exception as e:
        print(f"Error initializing Ollama LLM. Make sure Ollama is installed, running,")
        print(f"and the 'llama2' model is downloaded (e.g., by running 'ollama run llama2').")
        print(f"Error details: {e}")
        return

    parser = JsonOutputParser(pydantic_object=CapitalInfo)

    # Define a prompt template
    # This makes it easy to structure your prompts
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI assistant. Answer the user's questions concisely."),
        ("system", "the answer must be in json format"),
        ("user", "{question}")
    ]).partial(format_instructions=parser.get_format_instructions())

    # Define an output parser
    # This helps in getting the raw string output from the LLM
    #output_parser = StrOutputParser()

    # Create a simple chain
    # This connects the prompt, LLM, and output parser
    chain = prompt | llm | JsonOutputParser() 

    # Invoke the chain with a question
    question = "What is the capital of France?"
    print(f"Asking the LLM: '{question}'")
    response = chain.invoke({"question": question})
    print(f"LLM's Answer: {response}")

    print("\n--- Another example ---")
    question_2 = "Tell me a short, funny joke about a computer.give the output in JSON format"
    print(f"Asking the LLM: '{question_2}'")
    response_2 = chain.invoke({"question": question_2})
    print(f"LLM's Answer: {response_2}")

if __name__ == "__main__":
    run_basic_llm_example()





# output - 
LLM's Answer: {'answer': 'The capital of France is Paris.'}
