"""
this reads pdf files from a directory, and creates a chatbot to answer, uses chromadb vector
"""

from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma

# 1. Load documents from a folder
loader = DirectoryLoader("/Users/sankarbiswas/genai/chatbots/docs/chatbot1/", glob="**/*.pdf")  # or .txt/.pdf

"""
we could also use PyPDFLoader or UnstructuredPDFLoader, DirectoryLoader is a generic utility in LangChain that loads all files from a directory

-- you use PyPDFLoader, when you have text based pdfs

from langchain.document_loaders import PyPDFLoader
loader = PyPDFLoader("sample.pdf")


-- you use UnstructuredPDFLoader when your pdf contains complex formatting, images, or are scanned

from langchain.document_loaders import UnstructuredPDFLoader
loader = UnstructuredPDFLoader("sample.pdf")
docs = loader.load()

"""

documents = loader.load()

# 2. Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.split_documents(documents)

# 3. Create embeddings and save to Chroma
embedding = OllamaEmbeddings(model="llama2")
vectordb = Chroma.from_documents(docs, embedding, persist_directory="./chromadb")
vectordb.persist()

########################################################################

from langchain.llms import Ollama
from langchain.prompts import ChatPromptTemplate
from langchain.chains import RetrievalQA

# LLM setup
llm = Ollama(model="llama2")

# Prompt setup
prompt = ChatPromptTemplate.from_template("""
You are a helpful assistant. Use the following context to answer:

<context>
{context}
</context>

Question: {question}
Answer:
""")

# RetrievalQA Chain
retriever = vectordb.as_retriever()

rag_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",  # you can also use "map_reduce" or "refine"
    chain_type_kwargs={"prompt": prompt}
)


######################################################
# it will keep running 
while True:
    query = input("Ask something (or 'exit'): ")
    if query.lower() == "exit":
        break
    response = rag_chain.run(query)
    print("\n", response, "\n")
