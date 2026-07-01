# 🏡 1Beegha AI Real Estate Chatbot

An AI-powered Real Estate Assistant built for **1Beegha** to help customers discover properties, compare projects, answer property-related questions, and capture qualified sales leads using **Retrieval-Augmented Generation (RAG)**.

The chatbot combines modern Large Language Models (LLMs), semantic search, vector databases, and conversational memory to provide accurate, context-aware responses while maintaining a seamless customer experience.

---

## ✨ Features

- 🤖 AI-powered conversational assistant
- 📚 Retrieval-Augmented Generation (RAG)
- 🔍 Semantic search with Qdrant Vector Database
- 💬 Multi-turn conversation memory
- 🏘️ Property & project recommendations
- 💰 Pricing and investment guidance
- 📍 Location-based property information
- 📝 Automated lead capture
- 📊 Google Sheets CRM integration
- 📈 LangSmith observability and tracing
- 🛡️ Guardrails to restrict off-domain queries
- ⚡ FastAPI backend
- 🎨 Modern responsive frontend
- ☁️ Production-ready deployment

---

# 🏗️ System Architecture

```
                        +----------------------+
                        |   Web Chat Widget    |
                        |   HTML • CSS • JS    |
                        +----------+-----------+
                                   |
                                   |
                                   ▼
                    +-----------------------------+
                    |      FastAPI Backend        |
                    +-----------------------------+
                    |                             |
                    |  Guardrails                 |
                    |  Conversation Memory        |
                    |  Lead Detection             |
                    |  RAG Pipeline               |
                    |                             |
                    +-------------+---------------+
                                  |
                 +----------------+----------------+
                 |                                 |
                 ▼                                 ▼
      OpenAI GPT-4.1 Mini                 Qdrant Vector DB
                 |                                 |
                 +---------------+-----------------+
                                 |
                                 ▼
                       Company Knowledge Base
                     (PDFs, Website, Brochures)

                                 |
                                 ▼
                    LangSmith Monitoring & Tracing
                                 |
                                 ▼

                       Google Sheets (Lead CRM)
```

---

# 🚀 Tech Stack

## Backend

- FastAPI
- Python
- LangChain
- OpenAI GPT-4.1 Mini
- OpenAI Embeddings
- Qdrant Vector Database
- LangSmith
- Pydantic
- gspread
- Google Sheets API

---

## Frontend

- HTML5
- CSS3
- Vanilla JavaScript
- Font Awesome
- Google Fonts

---

## AI Components

- Retrieval-Augmented Generation (RAG)
- Semantic Search
- Vector Embeddings
- Conversational Memory
- Structured Lead Extraction
- Prompt Engineering
- LangSmith Observability

---

## Deployment

- WordPress Integration
- Qdrant Cloud
- GitHub

---

# 🧠 AI Workflow

```
User Query
      │
      ▼
 Guardrails
      │
      ▼
Conversation Memory
      │
      ▼
Lead Detection
      │
      ▼
Semantic Retrieval
      │
      ▼
Qdrant Search
      │
      ▼
Retrieved Context
      │
      ▼
OpenAI GPT-4.1 Mini
      │
      ▼
Final Response
      │
      ▼
Lead Saved to Google Sheets
```

---

# 🛡️ Guardrails

The chatbot is intentionally restricted to company and real-estate-related queries.

It refuses requests related to:

- Programming
- Medical advice
- Politics
- Religion
- Mathematics
- General knowledge outside the company's domain

This ensures reliable and domain-specific responses.

---

# 📊 Lead Management

Interested customers are automatically identified.

The chatbot collects:

- Name
- Phone Number
- Property Requirement

Qualified leads are securely stored in **Google Sheets** for the sales team.

---

# 🔍 Retrieval-Augmented Generation (RAG)

Instead of relying solely on an LLM, the chatbot retrieves relevant information from the company's knowledge base.

Knowledge Sources include:

- Property Brochures
- Project PDFs
- Pricing Documents
- Website Content

This approach significantly improves factual accuracy and reduces hallucinations.

---

# 📈 LangSmith Observability

The chatbot integrates **LangSmith** to monitor and trace the complete RAG pipeline.

It provides:

- End-to-end execution tracing
- Prompt inspection
- LLM response monitoring
- Retrieval debugging
- Latency analysis
- Error tracking
- Production observability

LangSmith enables faster debugging, performance optimization, and better reliability during development and deployment.

---


# 📈 Future Improvements

- Hybrid Search
- Cross Encoder Reranking
- Metadata Filtering
- Redis Memory
- Admin Dashboard
- Analytics
- WhatsApp Integration
- Voice Assistant
- Multi-language Support

---

# 🤝 Contributing

Contributions are welcome.

Please open an issue before submitting major changes.

---

# 👨‍💻 Author

**Ilham Khan**

Generative Ai Developer

B.Tech Computer Science Engineering

---

## ⭐ If you found this project useful, consider giving it a star.