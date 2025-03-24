import os
import wandb
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_pinecone import PineconeVectorStore
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone, ServerlessSpec

# Load environment variables
load_dotenv()

# Initialize wandb
wandb.init(project="rag-pipeline", name="llm-invocations", mode="online")

# Initialize Pinecone vector store
def get_retriever():
    index_name = 'call-agent-ai-2'  # Load from env
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2",
    )
    docsearch = PineconeVectorStore.from_existing_index(
        index_name=index_name,
        embedding=embeddings
    )
    return docsearch.as_retriever(search_kwargs={'k': 2})

# Initialize Groq LLM
def get_llm():
    # Ensure wandb is initialized before updating config
    if wandb.run is None:
        wandb.init(project="rag-pipeline", name="llm-invocations", mode="online")

    # Check if GROQ_API_KEY is set
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY is not set in the environment.")

    # Initialize Groq LLM
    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        temperature=0.9,
        api_key=groq_api_key,
        max_tokens=512
    )

    # Log model configuration to wandb
    wandb.config.update({
        "model_name": "llama-3.3-70b-versatile",
        "temperature": 0.9,
        "max_tokens": 512,
        "max_retries": 2
    })

    print("✅ Groq LLM initialized and logged to wandb.")
    return llm

# Create the Retrieval Augmented Generation (RAG) chain
def create_rag_chain(retriever, llm):
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )

# Example Usage
if __name__ == "__main__":
    llm = get_llm()
    if llm:
        print("LLM initialized successfully!")
    else:
        print("Failed to initialize LLM.")