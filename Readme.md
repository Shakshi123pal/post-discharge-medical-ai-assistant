Post-Discharge Medical AI Assistant (RAG + LangGraph)

For educational use only. Not for clinical decision-making.

This project implements a lightweight medical assistance system designed for post-discharge patients. It uses LangGraph to route between a Receptionist Agent (identity + triage) and a Clinical Agent (RAG over nephrology textbook + web fallback). A FastAPI backend and Streamlit UI provide a clean, demo-ready experience.

##  Key Features

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

##  Architecture Overview

The system follows a simple multi-agent pipeline:

User  
 → Streamlit UI  
 → FastAPI backend (/chat)  
 → LangGraph workflow  
       ├── Receptionist Agent  
       │     • Identifies patient  
       │     • Retrieves discharge report (PatientDB)  
       │     • Asks follow-up question  
       │     • Routes medical queries  
       │  
       └── Clinical Agent  
             • RAG over nephrology reference (ChromaDB)  
             • Web search fallback (DuckDuckGo)  
             • Returns answer + citations  

The final response is sent back to Streamlit UI for display.


## Repository Structure

```
datasmith-pdc-assistant/
│
├── app/
│   ├── main.py            # FastAPI app + /chat route
│   ├── graph.py           # LangGraph workflow
│   ├── schemas.py         # Pydantic models
│   ├── logging_conf.py    # JSON + file logging
│   ├── tools/
│   │   ├── patient_db.py  # Patient lookup tool
│   │   ├── rag_tool.py    # RAG search tool
│   │   └── web_search.py  # Web fallback tool
│   └── rag/store/         # ChromaDB (generated, ignored in Git)
│
├── Scripts/
│   ├── ingest_pdf.py      # PDF chunk + embedding
│   └── make_dummy_patients.py
│
├── data/
│   ├── patients.jsonl
│   └── comprehensive-clinical-nephrology.pdf
│
├── frontend/
│   └── app.py             # Streamlit UI
│
├── tests/
│   └── smoke_test.py
│
├── README.md
├── BRIEF_REPORT.md
├── .env.example
└── requirements.txt
```



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
