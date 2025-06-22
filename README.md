# 🏡 AI-Powered Real Estate Search Platform

An intelligent, multilingual real estate search engine powered by **LangGraph**, **Milvus**, **MongoDB**, **Guardrails**, and **RAG-based Semantic Search**. Built for high scalability, this project enables users to extract structured property data, search listings using natural language, and validate outputs using LLMs and Guardrails.

---

## 🔥 Features

- 🌐 **Multilingual Search** using MarianMT + RAG
- 🧠 **LangGraph-based LLM pipeline** for structured data extraction and reasoning
- 🏷️ **Guardrails** integration for output validation (e.g., profanity, structure)
- 🔎 **Milvus Vector DB** for semantic similarity search
- 📦 **MongoDB** for structured listing storage
- 🚀 **FastAPI + Uvicorn** backend
- 🐳 **Dockerized with Compose** (easy deployment)
- ☁️ **Ready for cloud deployment on Render**

---

## ⚙️ Tech Stack

| Layer           | Tech                                                                 |
|----------------|----------------------------------------------------------------------|
| Backend         | Python, FastAPI, LangGraph, LangChain                               |
| AI & NLP        | OpenAI GPT, MarianMT, SentenceTransformers                          |
| Vector DB       | Milvus (Standalone)                                                  |
| Database        | MongoDB                                                              |
| Validation      | Guardrails                                                           |
| Deployment      | Docker, Docker Compose, Render                                       |

---

## 📦 Project Structure

real-estate-llm/
├── app/
│ ├── guardrails_output.py # Guardrails validation logic
│ ├── translator.py # MarianMT translation
│ └── utils.py # Logging and helper functions
├── src/
│ └── extract_property_data.py # Main data extraction & embedding logic
├── cli_main.py # Entrypoint FastAPI app
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── wait-for-services.sh
└── README.md


---

## 🚀 Deployment

### ✅ Run Locally (with Docker Compose)

```bash
git clone https://github.com/<your-username>/real-estate-llm.git
cd real-estate-llm
docker compose up --build
