
# import pinecone
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain_core.vectorstores import InMemoryVectorStore
# from langchain.text_splitter import CharacterTextSplitter
# from langchain.text_splitter import RecursiveCharacterTextSplitter


# def vector_index():
#     embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

#     vector_store = InMemoryVectorStore(embeddings)

#     content = ""
#     with open("product_info.txt", "r") as f:
#         content = f.read()
#     # print(content)

#     text_splitter = CharacterTextSplitter(
#     separator="\n",
#     chunk_size=250, 
#     chunk_overlap=50
# )

#     chunks = text_splitter.split_text(content)

#     vector_store = FAISS.from_texts(texts=chunks, embedding=embeddings)

#     vector_store.save_local("vector_store/knowledge_base")


# if __name__ == "__main__":
#     vector_index()
  
  
import os
import pinecone
from pinecone import Pinecone
from pinecone import ServerlessSpec
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_pinecone import PineconeVectorStore

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