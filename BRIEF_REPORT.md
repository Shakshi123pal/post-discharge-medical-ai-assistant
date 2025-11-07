Technical Brief — Post-Discharge Medical AI Assistant
1. Problem

Patients discharged from hospitals often forget instructions, miss warning signs, or misunderstand symptoms. The goal is to develop a minimal, safe system that:

retrieves the patient's discharge data,

answers follow-up questions,

provides verified nephrology information using RAG,

and falls back to web search when the reference text is insufficient.

2. Approach

We designed a two-agent architecture using LangGraph:

✅ Receptionist Agent

Checks if the user has given a name

Verifies patient identity

Retrieves discharge details

Routes conversation to clinical agent if symptoms are mentioned

✅ Clinical Agent

Extracts clinical context

Runs RAG over Comprehensive Clinical Nephrology (7e)

Provides grounded, cited responses

Falls back to DuckDuckGo when needed

3. Knowledge Base Construction

PDF cleaned and chunked into ~12k segments

Embeddings generated using all-MiniLM-L6-v2

Indexed via ChromaDB with batch ingestion

Chunks include metadata:

source = textbook

page_hint = chunk index

4. DAG Architecture (LangGraph)
START
  │
  ▼
Receptionist Agent
  │ is_clinical?
  ├── NO → respond as receptionist
  └── YES
         │
         ▼
    Clinical Agent
     (RAG / Web Fallback)
  │
END


Benefits:

Deterministic routing

Highly debuggable

Easy to expand (add pharmacy/lab agents)

5. Tools
✅ Patient Data Tool

Retrieves synthetic patient report (diagnosis, labs, dates).

✅ RAG Tool

ChromaDB + MiniLM embeddings for fast semantic search.

✅ Web Search Tool

DuckDuckGo with safe search.

6. System Interface

FastAPI backend exposes /chat

Streamlit frontend

JSON logs for every turn

7. Safety Measures

No prescribing, no diagnosis

Pure reference-based responses

Citations displayed

Transparent fallback

Educational use disclaimers

8. Evaluation

Smoke tests ensure:

Identity missing → receptionist prompt

Valid patient name → record retrieval

Symptom message → clinical routing

RAG available → reference source

No RAG hit → web fallback

9. Future Work

Add symptom classifier

Add small LLM for summarization

Add patient history timeline view

Add monitoring dashboards

✅ Conclusion

The submission delivers a clean, modular, safe, and production-style mini-assistant. The architecture is extensible, transparent, and grounded in an authoritative reference. All mandatory features have been implemented and verified.