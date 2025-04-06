from langchain.schema import AIMessage, HumanMessage
from langchain.memory import ConversationBufferMemory

class Agent:
    def _init_(self, name, model, description, add_history_to_messages=True, num_history_responses=5):
        """
        Initializes an AI agent for handling conversations.
        """
        self.name = name
        self.model = model  # Groq model
        self.description = description
        self.memory = ConversationBufferMemory()
        self.add_history_to_messages = add_history_to_messages
        self.num_history_responses = num_history_responses

    def run(self, prompt):
        """
        Generates a response from the AI model.
        """
        if self.add_history_to_messages:
            conversation_history = self.memory.load_memory_variables({})["history"]
            full_prompt = f"{conversation_history}\n{prompt}"
        else:
            full_prompt = prompt

        response = self.model.invoke(full_prompt)
        
        # Save conversation
        self.memory.save_context({"input": prompt}, {"output": response.content})

        return AIMessage(content=response.content)