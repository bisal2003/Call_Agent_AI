import os
import pinecone
from pinecone import Pinecone
from pinecone import ServerlessSpec
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
load_dotenv()

def get_retriever():
    # Initialize Pinecone
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    
    # Initialize embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    
    # Connect to the existing Pinecone index
    index_name = "call-agent-ai"  # Replace with your index name
    docsearch = PineconeVectorStore.from_existing_index(
        index_name=index_name,
        embedding=embeddings
    )
    
    return docsearch.as_retriever(search_kwargs={'k': 2})

def vector_index():
    # Initialize embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    
    # Load content from text file
    with open("product_info.txt", "r") as f:
        content = f.read()
    
    # Split text into chunks
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=250, 
        chunk_overlap=50
    )
    chunks = text_splitter.split_text(content)
    
    # Initialize Pinecone
    
    api_key=os.getenv('PINECONE_API_KEY'),  # Set your API key in environment variables
    pc = Pinecone(api_key)
    
    # Upsert vectors to existing Pinecone index
    PineconeVectorStore.from_texts(
        texts=chunks,
        embedding=embeddings,
        index_name="call-agent-ai"  # Your existing index name
    )

if __name__ == "__main__":
    vector_index()