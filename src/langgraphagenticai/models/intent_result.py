from pydantic import BaseModel

class IntentResult(BaseModel):
    is_relevant: str
    response_message: str