import os
import wandb
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

# Function to initialize Groq LLM and log to wandb
def get_llm():
    try:
        # Ensure wandb API key is set
        wandb_api_key = os.getenv("WANDB_API_KEY")
        if not wandb_api_key:
            raise ValueError("WANDB_API_KEY is not set in the environment.")

        # Initialize wandb if not already initialized
        if wandb.run is None:
            wandb.login(key=wandb_api_key)
            wandb.init(project="rag-pipeline", name="llm-invocations", mode="online")

        # Ensure Groq API key is set
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

    except Exception as e:
        print(f"❌ Error initializing Groq LLM: {e}")
        return None
