from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

class Groq:
    def _init_(self, id="llama-3.3-70b-versatile"):
        """
        Initializes the Groq model.
        """
        self.model = ChatGroq(
            model_name=id,
            temperature=0.9,
            api_key=os.getenv("GROQ_API_KEY"),
            max_tokens=512
        )

    def invoke(self, prompt):
        """
        Generates a response from the Groq model.
        """
        return self.model.invoke(prompt)