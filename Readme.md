Post-Discharge Medical AI Assistant (RAG + LangGraph)

For educational use only. Not for clinical decision-making.

This project implements a lightweight medical assistance system designed for post-discharge patients. It uses LangGraph to route between a Receptionist Agent (identity + triage) and a Clinical Agent (RAG over nephrology textbook + web fallback). A FastAPI backend and Streamlit UI provide a clean, demo-ready experience.

✅ Key Features

25+ synthetic patient records (JSONL)

Nephrology RAG using Comprehensive Clinical Nephrology (7e)

Chunked embedding indexing with ChromaDB

Receptionist agent (identity + record lookup)

Clinical agent (RAG → web fallback)

DuckDuckGo web search

Structured logging (JSON)

Streamlit web UI

FastAPI backend

LangGraph DAG-based workflow

Batch ingestion for large PDFs

Citations shown for each RAG answer

Separation of concerns in clean module structure

✅ Architecture Overview
                                ┌───────────────────────────┐
                                │            User            │
                                │  • Enters name             │
                                │  • Sends message / query   │
                                └──────────────┬─────────────┘
                                               │ (1)
                                               │ User input
                                               ▼
                                ┌───────────────────────────┐
                                │        Streamlit UI       │
                                │  • Collects input          │
                                │  • Sends POST /chat        │
                                └──────────────┬─────────────┘
                                               │ (2)
                           POST /chat JSON:    │
                           {                    │
                             "user_name": "...",
                             "user_message": "..."
                           }
                                               ▼
                       ┌──────────────────────────────────────────┐
                       │               FastAPI Backend            │
                       │     /chat → calls LangGraph workflow     │
                       └──────────────┬───────────────────────────┘
                                      │ (3)
                                      ▼
                          ┌────────────────────────┐
                          │     LangGraph DAG      │
                          │  (Conversation Engine) │
                          └──────────┬─────────────┘
                                     │ Route based on message
     ┌──────────────────────────────┬┴───────────────────────────────┐
     │                              │                                │
     ▼                              ▼                                ▼
┌────────────────┐         ┌────────────────────┐        ┌────────────────────────────┐
│Receptionist    │         │ Clinical Agent      │        │   Future Agents (optional) │
│Agent           │         │ (Medical Query)     │        │   • Pharmacy Agent         │
│• Identity check│         │ • Symptom analysis  │        │   • Billing Agent          │
│• Match patient │         │ • RAG over textbook │        │   • Lab Reports Agent      │
│• Greeting flow │         │ • Web fallback      │        │                            │
└───────┬────────┘         └───────────┬──────────┘        └────────────────────────────┘
        │ (4)                           │ (5)
        ▼                               ▼
┌────────────────┐             ┌──────────────────────────────┐
│ PatientDB      │             │   RAG Engine (ChromaDB)       │
│ local JSONL    │             │ • MiniLM embeddings           │
│ • Diagnosis    │             │ • Chunked nephrology text     │
│ • Medications  │             │ • Citation metadata           │
└────────────────┘             └──────────┬────────────────────┘
                                          │ (6) If no RAG match
                                          ▼
                            ┌──────────────────────────────────┐
                            │     DuckDuckGo Web Search Tool   │
                            │ • Retrieves latest medical info  │
                            └──────────────────────────────────┘

                                               │
                                               ▼
                     ┌──────────────────────────────────────────┐
                     │     FastAPI returns structured JSON      │
                     │   { answer, from_source, citations,... } │
                     └──────────────────────────────────────────┘
                                               │ (7)
                                               ▼
                                ┌───────────────────────────┐
                                │        Streamlit UI       │
                                │  • Shows answer            │
                                │  • Shows citations         │
                                └──────────────┬─────────────┘
                                               │ (8)
                                               ▼
                                ┌───────────────────────────┐
                                │            User            │
                                │   Reads final response     │
                                └───────────────────────────┘

✅ Repository Structure
datasmith-pdc-assistant/
│
├── app/
│   ├── main.py                # FastAPI app + endpoint
│   ├── graph.py               # LangGraph workflow
│   ├── schemas.py             # Pydantic models
│   ├── logging_conf.py        # JSON logging
│   └── tools/
│       ├── patient_db.py      # Patient lookup tool
│       ├── rag_tool.py        # RAG search tool
│       └── web_search.py      # Web fallback tool
│
├── app/rag/store/             # ChromaDB vector store (autogenerated)
│
├── Scripts/
│   ├── ingest_pdf.py          # Chunk + embed PDF into ChromaDB
│   └── make_dummy_patients.py # Generate 30 synthetic patient reports
│
├── data/
│   ├── patients.jsonl
│   └── comprehensive-clinical-nephrology.pdf
│
├── frontend/
│   └── app.py                 # Streamlit UI
│
├── tests/
│   └── smoke_test.py
│
├── .env.example
├── requirements.txt
├── README.md
└── BRIEF_REPORT.md

✅ Setup Instructions
1. Create Virtual Environment
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

✅ Data Preparation
1️⃣ Generate dummy patient data
python Scripts/make_dummy_patients.py

2️⃣ Build RAG vector store
python Scripts/ingest_pdf.py --pdf data/comprehensive-clinical-nephrology.pdf


This creates the Chroma vector store at:

app/rag/store/

✅ Running the App
Start Backend
uvicorn app.main:api --reload --port 8000


Swagger Docs:
👉 http://localhost:8000/docs

Start UI
streamlit run frontend/app.py


UI opens at:
👉 http://localhost:8501

✅ API Endpoint
POST /chat

Input:

{
  "user_name": "Ravi Kumar",
  "user_message": "I have leg swelling"
}


Output:

{
  "answer": "...",
  "from_source": "reference | web",
  "citations": [...],
  "patient_found": true
}

✅ Logging

Every turn produces structured logs:

{
  "event": "chat_turn",
  "route": "clinical",
  "from_source": "reference",
  "citations": ["chunk_888", "chunk_1638"]
}

✅ Testing
pytest -q


Smoke tests cover:

missing name

patient lookup

clinical handoff RAG/web

✅ License

For educational demonstration only.