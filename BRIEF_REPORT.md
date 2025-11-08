# Technical Brief — Post-Discharge Medical AI Assistant

## 1. Problem

Post-discharge patients often:

- forget instructions  
- miss early warning signs  
- misunderstand symptoms  
- fail to follow medication schedules  

This project delivers a minimal, safe AI system that:

- retrieves patient discharge data  
- answers follow-up questions  
- provides nephrology-grounded answers using RAG  
- uses web search when textbook info is insufficient  

---

## 2. Approach

We designed a **two-agent LangGraph architecture**:

###  Receptionist Agent
- Checks if the user has provided a name  
- Verifies patient identity  
- Retrieves the patient's discharge report  
- Asks follow-up questions based on report  
- Routes clinical messages to the Clinical Agent  

###  Clinical Agent
- Extracts medical intent  
- Runs RAG over *Comprehensive Clinical Nephrology (7e)*  
- Provides grounded, citation-backed answers  
- Uses DuckDuckGo for questions outside the reference  
- Returns structured response + citations  

---

## 3. Knowledge Base Construction

- Nephrology PDF cleaned and chunked into **~12,140 segments**  
- MiniLM (`all-MiniLM-L6-v2`) used for embeddings  
- Indexed with **ChromaDB** (batch ingestion enabled)  
- Each chunk stored with metadata:

```
{
  "source": "textbook",
  "chunk_id": 4723,
  "page_hint": "approximate location"
}
```

---

## 4. LangGraph DAG Architecture

```
START
  │
  ▼
Receptionist Agent
  │ is_clinical?
  ├── NO  → receptionist response
  └── YES → Clinical Agent
                 │
                 ▼
         RAG → or → Web Fallback
                 │
                END
```

**Benefits:**
- Deterministic routing  
- High debuggability  
- Easy to extend with more agents (pharmacy, labs, billing)  

---

## 5. Tools

###  Patient Data Tool  
- Retrieves synthetic patient records (diagnosis, meds, dates, warnings)

###  RAG Tool  
- ChromaDB + MiniLM embeddings  
- Fast semantic search over nephrology reference  

###  Web Search Tool  
- DuckDuckGo API  
- Used only when RAG confidence is low  

---

## 6. System Interface

- **FastAPI backend** exposes the `/chat` endpoint  
- **Streamlit frontend** provides user-facing UI  
- **JSON logs** for every turn  
- Logging includes: routing, citations, patient lookup, tools used  

---

## 7. Safety Measures

- No prescribing or diagnosis  
- Purely reference-based information  
- Citations shown transparently  
- Web results clearly labelled  
- "Educational use only" warnings added  

---

## 8. Evaluation

Basic smoke tests validate:

- Missing name → receptionist requests identity  
- Valid patient → correct discharge report retrieval  
- Symptom message → routed to Clinical Agent  
- RAG hit → “reference” + citations returned  
- No RAG hit → Web search fallback  

All core functionality works end-to-end.

---

## 9. Future Work

- Add lightweight symptom classifier  
- Add mini-LLM summarization  
- Add longitudinal patient timeline  
- Monitoring dashboards and analytics  

---

##  Conclusion

This submission provides a **clean, modular, safe, production-style mini-assistant**.  
The system is grounded in a trusted nephrology reference, uses clear agent routing,  
and delivers all mandatory assignment features — fully implemented and verified.

