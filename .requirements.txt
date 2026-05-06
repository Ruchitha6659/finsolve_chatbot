# 💬 FinSolve Chatbot — AI-Powered Internal Assistant

![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-VectorStore-orange?style=for-the-badge)
![Groq](https://img.shields.io/badge/Groq-LLM-purple?style=for-the-badge)
![LangChain](https://img.shields.io/badge/LangChain-RAG-green?style=for-the-badge)

> **An RBAC-enabled RAG chatbot for FinSolve Technologies — answers internal questions using company documents, with role-based access control.**

---

## 🚀 Project Overview

**FinSolve Chatbot** is a production-grade internal AI assistant built for FinSolve Technologies Inc. It uses **Retrieval-Augmented Generation (RAG)** to answer questions based on internal company documents — finance reports, HR policies, marketing data, and engineering docs. Access is strictly controlled via **Role-Based Access Control (RBAC)**, ensuring employees only see data relevant to their role.

---

## ❗ Problem Statement

| Problem | Impact |
|---|---|
| 📄 **Scattered internal documents** across departments | Hard to find the right information quickly |
| 🔒 **No access control** on sensitive data | Finance data visible to all employees |
| 🤖 **No AI assistant** for internal queries | Employees waste time searching manually |
| 📊 **Manual report reading** for financial queries | Slow decision-making process |

---

## 💡 Solution

- ✅ **Role-Based Access**: Finance team sees only finance docs, HR sees only HR docs
- ✅ **RAG Pipeline**: Answers are grounded in actual company documents
- ✅ **Source Citations**: Every answer includes the source document
- ✅ **Secure Login**: Authentication with role assignment
- ✅ **Streamlit UI**: Clean, user-friendly chat interface

---

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit |
| **Backend** | FastAPI |
| **LLM** | Groq API (LLaMA 3.3 70B Versatile) |
| **Embeddings** | HuggingFace (all-MiniLM-L6-v2) |
| **Vector Store** | ChromaDB |
| **RAG Framework** | LangChain |
| **Language** | Python 3.11 |

---

## 👥 RBAC Role Hierarchy

| Role | Access |
|---|---|
| `c_level` | All departments |
| `finance` | Finance + General |
| `hr` | HR + General |
| `marketing` | Marketing + General |
| `engineering` | Engineering + General |
| `employee` | General only |

---

## 📁 Project Structure

```
finsolve_chatbot/
├── backend/
│   ├── main.py       # FastAPI app
│   ├── rag.py        # RAG pipeline
│   ├── ingest.py     # Document ingestion
│   ├── rbac.py       # RBAC logic
│   └── .env          # API keys (not committed)
├── frontend/
│   └── app.py        # Streamlit UI
├── data/
│   ├── finance/
│   ├── hr/
│   ├── marketing/
│   ├── engineering/
│   └── general/
├── requirements.txt
└── README.md
```

---

## 🛠️ Local Setup Guide

### Step 1 — Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/finsolve-chatbot.git
cd finsolve-chatbot
```

### Step 2 — Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### Step 3 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Set Up Environment Variables
Create a `.env` file in the root folder:
```
GROQ_API_KEY=your_groq_api_key_here
```
Get your free Groq API key at: https://console.groq.com

### Step 5 — Add Your Documents
Place documents in the appropriate `data/` subfolders.
Supported formats: `.pdf`, `.csv`, `.xlsx`, `.txt`, `.md`

### Step 6 — Ingest Documents
```bash
cd backend
python ingest.py
```

### Step 7 — Start Backend (Terminal 1)
```bash
cd backend
uvicorn main:app --reload
```

### Step 8 — Start Frontend (Terminal 2)
```bash
cd frontend
python -m streamlit run app.py
```

### Step 9 — Open in Browser
```
http://localhost:8501
```

---

## 🔑 Test Credentials

| Username | Password | Role |
|---|---|---|
| alice | alice123 | finance |
| bob | bob123 | hr |
| charlie | charlie123 | marketing |
| diana | diana123 | engineering |
| eve | eve123 | c_level |
| frank | frank123 | employee |

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| POST | `/login` | Authenticate user |
| POST | `/chat` | Ask a question |
| GET | `/roles` | List all roles |

---

## ⚠️ Troubleshooting

| Error | Fix |
|---|---|
| `PermissionError on chroma_db` | Move project out of OneDrive |
| `Cannot connect to server` | Start backend with `uvicorn main:app --reload` |
| `I don't have access to that information` | Run `python ingest.py` first |
| `422 Unprocessable Entity` | Check request body fields |
| `File does not exist: app.py` | Make sure you are in the `frontend/` folder |

---

## 🚀 Future Improvements

| Feature | Description |
|---|---|
| 🔐 **JWT Authentication** | Replace hardcoded users with JWT tokens |
| 🗄️ **Real Database** | PostgreSQL for user management |
| ☁️ **Cloud Deployment** | Deploy on AWS/GCP with Docker |
| 📊 **Admin Dashboard** | Usage analytics and logs |

---


*FinSolve Chatbot — Because your internal data deserves an intelligent assistant.*
