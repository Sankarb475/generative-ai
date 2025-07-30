# 🧠 LLM Chatbot Framework – RAG Pipeline Overview

This repository demonstrates the foundational components of an LLM-powered chatbot using a Retrieval-Augmented Generation (RAG) architecture.

## 🔧 Components Overview

### 1. 📦 Output Parser
- **Purpose**: Converts LLM-generated text into a structured format (JSON, list, dict, etc.)
- **Use case**: Helps enforce consistent formatting for downstream processing (e.g., QA pairs, tables).
- **Tools**: `LangChain OutputParser`, `PydanticOutputParser`, `RegexParser`

### 2. ✂️ Chunking
- **Purpose**: Breaks large documents into manageable pieces for embedding & retrieval.
- **Strategies**:
  - Fixed-size chunking (e.g., 500 tokens)
  - Overlapping windows (e.g., 500 tokens with 50 overlap)
  - Semantic chunking (based on headers or topic shifts)
- **Tools**: `LangChain TextSplitter`, `RecursiveCharacterTextSplitter`

### 3. 📚 Vector Database (Vector DB)
- **Purpose**: Stores document chunks as vector embeddings for semantic search.
- **Workflow**:
  - Text → Embeddings → Stored in vector DB
  - Query → Embedding → Nearest neighbors → Retrieved chunks
- **Common Vector DBs**:
  - `FAISS` (local)
  - `ChromaDB`
  - `Pinecone`, `Weaviate` (hosted)

### 4. 🤖 Chatbot
- **Purpose**: Enables conversation interface for users to ask questions based on stored knowledge.
- **Workflow**:
  - User query → Query transformation → Vector DB search → LLM → Answer
- **Tools**:
  - `Streamlit` for UI
  - `LangChain ConversationalRetrievalChain`
  - `Ollama` / `HuggingFace` / `OpenAI` for LLM backend

### 5. 🔄 Query Transformation
- **Purpose**: Reformulates user queries to better match context/document structure.
- **Examples**:
  - Convert "Tell me about policies" → "Summarize the company HR policies."
- **Tools**:
  - `PromptTemplates` + LLM-based rewriters
  - Query Rewriter Chains in LangChain
