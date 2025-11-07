from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Optional, List, Dict
from app.tools.patient_db import PatientDB
from app.tools.rag_tool import NephroRAG
from app.tools.web_search import web_search

class ChatState(TypedDict):
    user_name: Optional[str]
    user_message: str
    patient_record: Optional[Dict]
    route: Optional[str]           # "reception" or "clinical"
    retrieved: Optional[List[Dict]]
    citations: Optional[List[Dict]]
    answer: Optional[str]
    from_source: Optional[str]     # "reference" | "web"

pdb = PatientDB()
rag = NephroRAG()

def receptionist_node(state: ChatState) -> ChatState:
    if not state.get("user_name"):
        return {**state, "answer": "Hello! I'm your post-discharge assistant. What's your name?", "route":"reception"}
    # fetch record
    status, data = pdb.lookup(state["user_name"])
    if status=="not_found":
        return {**state, "answer": "I couldn't find your record. Please re-check the spelling.", "route":"reception"}
    if status=="multiple":
        return {**state, "answer": f"Multiple matches found: {', '.join(data['candidates'])}. Please specify full name.", "route":"reception"}
    # basic triage: if message looks clinical, handoff
    msg = (state.get("user_message") or "").lower()
    clinical_trigger = any(w in msg for w in ["pain","swelling","dose","medicine","symptom","urine","shortness","diet"])
    if clinical_trigger:
        return {**state, "patient_record": data, "route":"clinical"}
    # otherwise receptionist follow-ups
    follow = f"Hi {data['patient_name']}! I found your report dated {data['discharge_date']} for {data['primary_diagnosis']}. Are you following your medications?"
    return {**state, "patient_record": data, "answer": follow, "route":"reception"}

def clinical_node(state: ChatState) -> ChatState:
    q = state["user_message"]
    # try RAG first
    results = rag.search(q, k=4)
    if results:
        cited = "\n".join([f"- {r['source']} (chunk {r['page_hint']})" for r in results])
        ans = f"From nephrology reference:\n{results[0]['text']}\n\nCitations:\n{cited}"
        return {**state, "retrieved":results, "citations":results, "answer":ans, "from_source":"reference"}
    # fallback to web
    hits = web_search(q, max_results=3)
    brief = "\n".join([f"- {h['title']} — {h['href']}" for h in hits])
    ans = f"This needed up-to-date info, so I searched the web:\n{brief}"
    return {**state, "citations":hits, "answer":ans, "from_source":"web"}

graph = StateGraph(ChatState)
graph.add_node("receptionist", receptionist_node)
graph.add_node("clinical", clinical_node)

# edges
graph.add_edge(START, "receptionist")
graph.add_conditional_edges("receptionist", lambda s: "clinical" if s.get("route")=="clinical" else END, {"clinical":"clinical", END:END})
graph.add_edge("clinical", END)

workflow = graph.compile()
