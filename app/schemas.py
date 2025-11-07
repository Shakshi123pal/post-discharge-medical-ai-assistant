from pydantic import BaseModel
from typing import Optional, List, Dict

class ChatIn(BaseModel):
    user_name: Optional[str] = None
    user_message: str

class ChatOut(BaseModel):
    answer: str
    from_source: Optional[str] = None
    citations: Optional[List[Dict]] = None
    patient_found: Optional[bool] = None
