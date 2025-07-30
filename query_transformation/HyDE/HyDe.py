import os
import chromadb
from chromadb.utils import embedding_functions
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.documents import Document
from langchain_core.runnables import Runnable, RunnablePassthrough # Import Runnable
from llm_setup import get_llm, setup_rag_components
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.embeddings import OllamaEmbeddings

"""
HyDe (Hypothetical document embeddings) - here we send the user query to an LLM first which returns a hypothetical ideal answer which expands the user query, and 
adds context. 
This generated content then converted to embeddings and used to search in vector db for better outcome
"""

print("\n--- Running HyDE Example ---")

# Call the setup function to get LLM, vectorstore, and combine_docs_chain
llm, vectorstore, combine_docs_chain = setup_rag_components()

# Check if setup was successful
if llm is None or vectorstore is None or combine_docs_chain is None:
    print("Failed to set up RAG components. Exiting.")
    exit()

# Define the prompt for generating a hypothetical document
hyde_prompt_template_str = """Please write a concise, hypothetical answer to the following question.
This answer will be used to retrieve relevant documents, so make it comprehensive and keyword-rich:

Question: {question}

Hypothetical Answer:"""

hyde_prompt = PromptTemplate.from_template(hyde_prompt_template_str)
hyde_llm_chain = LLMChain(llm=llm, prompt=hyde_prompt)


# FIX: Implement the 'invoke' method directly, as required by Runnable
class HyDERetriever(Runnable): # Inherit from Runnable
    def __init__(self, vectorstore, hyde_llm_chain):
        self.vectorstore = vectorstore
        self.hyde_llm_chain = hyde_llm_chain
        # Ensure the underlying vectorstore's retriever is used for similarity search
        self.base_retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})

    # Renamed from _invoke to invoke
    def invoke(self, input: str, config=None): # input should be the query string
        # Generate hypothetical document using LLMChain.invoke and access 'text'
        hypothetical_answer_result = self.hyde_llm_chain.invoke({"question": input})
        hypothetical_answer = hypothetical_answer_result.get('text', '') # Safely get the text output

        print(f"\n[HyDE] Generated Hypothetical Answer:\n{hypothetical_answer}\n")

        # Use the base_retriever's invoke method which is tied to the vectorstore's embedding
        retrieved_docs = self.base_retriever.invoke(hypothetical_answer)
        return retrieved_docs

    # Optional: If you need to support batch processing, implement _batch_invoke
    # def _batch_invoke(self, inputs: list[str], config=None):
    #     return [self.invoke(input, config) for input in inputs]


# Instantiate the HyDE retriever
hyde_retriever = HyDERetriever(vectorstore, hyde_llm_chain)

# Create a RAG chain using the HyDE retriever
hyde_rag_chain = create_retrieval_chain(hyde_retriever, combine_docs_chain)

user_query = "What are the environmental impacts of burning fossil fuels?"
response = hyde_rag_chain.invoke({"input": user_query})

print(f"User Query: {user_query}")
print(f"RAG Answer (with HyDE): {response['answer']}")
print("\nRetrieved Documents (with HyDE):")
for doc in response['context']:
    print(f"- {doc.metadata.get('source', 'Unknown Source')}: {doc.page_content[:100]}...")
