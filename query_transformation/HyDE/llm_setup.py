import os
from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

# --- 1. Set up Ollama LLM and Embeddings ---
# create a Chroma vector database to store embeddings of your private data 
# Ensure Ollama server is running and you have pulled the desired model (e.g., 'llama3')

def get_llm(model_name):
    llm = ChatOllama(model=model_name, temperature=0.2) # Lower temperature for more deterministic outputs
    return llm

def setup_rag_components():
    # --- 2. Load and Chunk Documents (for RAG) ---
    # Create a 'data' directory and put your text files there
    llm = get_llm('llama3')
    embeddings = OllamaEmbeddings(model="llama3")

    data_dir = "/Users/sankarbiswas/genai/streamlit/repo/streamlit_intro/resources/query_transformations"
    documents = []
    for filename in os.listdir(data_dir):
        filepath = os.path.join(data_dir, filename)
        if os.path.isfile(filepath) and filepath.endswith(".txt"):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                documents.append(Document(page_content=content, metadata={"source": filename}))

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(documents)

    # --- 3. Create a Vector Store (ChromaDB for local) ---
    # This will create a local directory 'chroma_db' to store embeddings
    vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings, persist_directory="/Users/sankarbiswas/genai/streamlit/repo/streamlit_intro/pages/vector_dbs/chroma/query_transformations/v1/")
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3}) # Retrieve top 3 documents

    # --- 4. Basic RAG Chain for comparison ---
    # This chain will take a question and context and generate an answer
    qa_system_prompt = """You are an assistant for question-answering tasks.
    Use the following pieces of retrieved context to answer the question.
    If you don't know the answer, say that you don't know.
    Use three sentences maximum and keep the answer concise.
    
    {context}"""

    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", qa_system_prompt),
        ("human", "{input}"),
    ])

    combine_docs_chain = create_stuff_documents_chain(llm, qa_prompt)
    basic_rag_chain = create_retrieval_chain(retriever, combine_docs_chain)

    print("Setup complete!")
    return llm, vectorstore, combine_docs_chain
