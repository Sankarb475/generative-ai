"""
example of using FAISS.

efficient similarity search and clustering of dense vectors. It's not a full-fledged "database" in the traditional sense, but rather a powerful 
library that provides the core algorithms and data structures for vector search.

many databases leverage Faiss's underlying algorithms for their own vector search capabilities.

creates a persistent vector storage - 
(venv) sankarbiswas@EPINBANW069A faiss_chatbot % ls
faiss_chatbot1.py	faiss_index
(venv) sankarbiswas@EPINBANW069A faiss_chatbot % cd faiss_index 
(venv) sankarbiswas@EPINBANW069A faiss_index % ls
index.faiss	index.pkl

"""

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load your PDF
loader = PyPDFLoader("/Users/sankarbiswas/genai/chatbots/docs/chatbot1/databricks.pdf")
pages = loader.load()

# Split pages into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)
docs = splitter.split_documents(pages)


from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

# Load a local embedding model (or use OpenAI/BGE)
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Store embeddings into FAISS
vectorstore = FAISS.from_documents(docs, embedding)

# Save to disk (optional)
vectorstore.save_local("faiss_index")


retriever = vectorstore.as_retriever(search_kwargs={"k": 5})


from langchain.chat_models import ChatOllama
from langchain.chains import RetrievalQA
from langchain.prompts import ChatPromptTemplate

llm = ChatOllama(model="llama2")

# Optional custom prompt
prompt_template = ChatPromptTemplate.from_template("""
You are a helpful assistant. Use the following context to answer:
{context}

Question: {question}
""")

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",  # You can use "map_reduce" for large context
    retriever=retriever,
    return_source_documents=True
)


query = "What is the main objective of the document?"
result = qa_chain(query)

print(result["result"])
# Optional: print(result["source_documents"])

query = "VACUUM?"
result = qa_chain(query)

print(result["result"])
