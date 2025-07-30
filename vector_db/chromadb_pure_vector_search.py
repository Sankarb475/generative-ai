# this code is an example of pure vector search, where whatever information you will feed to the vector db, will be retrived as is 
# but while retrieval it will check which information is most closely aligning with the search query

# we have RAG = Retrieval + Generation together (using LLM), that will be in a different file


import chromadb
from sentence_transformers import SentenceTransformer

import os
from dotenv import load_dotenv

class ChromaExample:
    def __init__(self):
        # Initialize Chroma client (stores data locally)
        self.client = chromadb.Client()
        self.collection = self.client.create_collection("my_documents")
        
        # Initialize embedding model (runs locally, no API needed)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def add_documents(self, documents, ids=None):
        """Add documents to the vector database"""
        if ids is None:
            ids = [f"doc_{i}" for i in range(len(documents))]
        
        # Generate embeddings
        embeddings = self.model.encode(documents).tolist()
        
        # Add to Chroma
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            ids=ids
        )
        print(f"Added {len(documents)} documents to Chroma")
    
    def search(self, query, n_results=3):
        """Search for similar documents"""
        # Generate query embedding
        query_embedding = self.model.encode([query]).tolist()
        
        # Search
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )
        
        return results


def main():
    print("=== Vector Database Examples ===\n")
    
    # Sample documents
    documents = [
        "Sankar married to Dipsi",
        "they know each other from 2023, Decmber",
        "Dipsi is cute, pretty, and a fibre engineer working for amdocs",
        "Dipsi lives in Shyamnagar, west bengal",
        "Dipsi had an issue with his last company (CCI systems) supervisor Jay",
        "Dipsi has cyst on her right ovary, its 7 cms multiocculated"
    ]
    
    # Example 1: Chroma
    print("1. CHROMA EXAMPLE")
    print("-" * 30)
    chroma_db = ChromaExample()
    chroma_db.add_documents(documents)
    
    query = "Who is Jay to Dipsi?"
    results = chroma_db.search(query)
    print(f"Query: {query}")
    print("Results:")
    for i, doc in enumerate(results['documents'][0]):
        print(f"  {i+1}. {doc}")
    print()


if __name__ == "__main__":
    main()
