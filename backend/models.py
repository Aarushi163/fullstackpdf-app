from pydantic import BaseModel

class QuestionRequest(BaseModel):
    document_id: str
    question: str
