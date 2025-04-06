# 🚀 CALL.E - AI-Powered Bulk Calling Agent
**Winner of NEURATHON 2025 🏆**

CALL.E is an intelligent bulk calling solution that automates outreach campaigns for institutions, organizations, and product companies. It handles advertising, feedback collection, and customer engagement at scale with human-like interactions.

---

## 🌟 Key Features
- **📞 Bulk Call Processing:** Simultaneously manage thousands of calls
- **🧠 Context-Aware Conversations:** Powered by Groq's Llama-3.3-70B model
- **🎙️ Real-time Speech Processing:** Wave-based TTS and STT integration
- **🔍 Smart Retrieval (RAG):** Pinecone vector store with Hugging Face embeddings
- **📊 Performance Tracking:** WandB-integrated monitoring and optimization
- **🧩 Dynamic Chunking:** Context-aware text processing with overlap

---

## 🛠️ Tech Stack
| Component        | Technology                        |
|-----------------|--------------------------------|
| **LLM Backbone** | Groq (Llama-3.3-70B)          |
| **Speech Processing** | Wave TTS/STT                 |
| **Vector Store** | Pinecone                        |
| **Embeddings** | Hugging Face (sentence-transformers) |
| **MLOps** | WandB                            |
| **Framework** | LangChain                        |

---

## 🚀 Getting Started
### Prerequisites
- Python 3.9+
- Groq API Key
- Pinecone API Key
- WandB Account
- Wave API Key

![image](https://github.com/user-attachments/assets/fd6c6528-ffc7-4a4d-87be-de2c1f4927f5)


### Installation
```bash
# Clone repository
git clone https://github.com/yourusername/CALL.E.git

# Backend setup
cd backend
pip install -r requirements.txt

# Frontend Setup
cd ../frontend
npm install
```

### ⚙️ Configuration
Create a `.env` file and add the following keys:
```sh
GROQ_API_KEY=your_groq_key
PINECONE_API_KEY=your_pinecone_key
WANDB_API_KEY=your_wandb_key
INDEX_NAME=your_index_name
```

---

## 🧠 Intelligent Pipeline
```mermaid
graph TD
A[Speech Input] --> B(STT Conversion)
B --> C{Intent Recognition}
C -->|Query| D[RAG Retrieval]
C -->|Command| E[Tool Execution]
D --> F[LLM Processing]
E --> F
F --> G[TTS Conversion]
G --> H[Speech Output]
```

---

## 📂 Project Structure
```
CALL.E/
├── backend/            # Core AI components
│   ├── src/            # Source files
│   │   ├── chains.py   # Conversation workflows
│   │   ├── models.py   # LLM & Vector Store config
│   │   ├── tools.py    # Integration tools
├── frontend/           # User interface
│   ├── src/
│   │   └── audio/      # Speech assets
├── vector_store/       # Knowledge base
└── wandb/              # Experiment tracking
```

---

## 🏎️ Quick Start Example
```python
# Initialize AI agent
from src.models import get_retriever, create_rag_chain

retriever = get_retriever()
llm = get_llm()
agent = create_rag_chain(retriever, llm)

# Start conversation
response = agent.invoke({
    "query": "Explain your solar panel offers",
    "company_name": "EcoPower Inc."
})
print(response["result"])
```

---

## 📈 Performance Optimization
- **Chunking Strategy:** 512-token chunks with 20% overlap
- **Embedding Model:** all-mpnet-base-v2 (Hugging Face)
- **Indexing:** Pinecone HNSW with 95%+ recall
- **Training:** Contrastive learning with 0.0001 lr

![image](https://github.com/user-attachments/assets/90e60d18-2c0b-4af7-8655-73a80e36b0ad)


---

## 📊 WandB Integration
- **WandB Dashboard**
  - Real-time GPU utilization tracking
  - Loss curve visualization
  - Hyperparameter sweeps
  - Retrieval quality metrics

![WandB Dashboard](https://github.com/user-attachments/assets/38e2e7df-281e-419a-b7ce-e43f638d856c)

---
## Conclusion

CALL.E is a breakthrough in AI-powered bulk calling, enhancing large-scale communication with efficiency and precision. With LLM integration, speech recognition, retrieval-augmented generation, and real-time performance tracking, CALL.E stands as a premier solution for automated outreach. Its success at NEURATHON 2025 solidifies its impact on AI-driven customer interaction and scalability.



## 🏆 Acknowledgments
### **NEURATHON 2025 Winning Solution**
CALL.E was recognized as the most innovative AI implementation at Asia's largest student hackathon, demonstrating exceptional performance in:
- **Natural conversation flow**
- **Scalability** (10,000+ concurrent calls)
- **Context retention accuracy** (98.7%)
- **Ethical AI practices**

---

