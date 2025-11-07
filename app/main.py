from fastapi import FastAPI
from app.graph import workflow
from app.logging_conf import setup_json_logger
from app.schemas import ChatIn, ChatOut

api = FastAPI(title="Post-Discharge Assistant", version="0.1")
log = setup_json_logger()

@api.post("/chat", response_model=ChatOut)
def chat(payload: ChatIn):
    state = {
        "user_name": payload.user_name,
        "user_message": payload.user_message,
        "patient_record": None,
        "route": None,
        "retrieved": None,
        "citations": None,
        "answer": None,
        "from_source": None
    }
    result = workflow.invoke(state)
    log.info({
        "event":"chat_turn",
        "user_name": result.get("user_name"),
        "route": result.get("route"),
        "from_source": result.get("from_source"),
        "citations": result.get("citations")
    })
    return ChatOut(
        answer=result.get("answer") or "…",
        from_source=result.get("from_source"),
        citations=result.get("citations"),
        patient_found=bool(result.get("patient_record"))
    )
