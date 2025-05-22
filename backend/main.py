from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid

from qa_engine import process_pdf_and_build_index_background, answer_question, is_index_ready
from models import QuestionRequest

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        doc_id = str(uuid.uuid4())
        file_bytes = await file.read()
        filename = file.filename

        print(f"[UPLOAD] Received: {filename}, doc_id={doc_id}")
        process_pdf_and_build_index_background(doc_id, file_bytes)  
        print(f"[UPLOAD] Index created for doc_id={doc_id}")
        return {"document_id": doc_id}
    except Exception as e:
        print(f"[UPLOAD ERROR] {str(e)}")
        return {"error": str(e)}

@app.post("/ask")
async def ask_question(data: QuestionRequest):
    try:
        answer = answer_question(data.document_id, data.question)
        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}
