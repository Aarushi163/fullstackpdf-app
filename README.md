AI-Powered PDF Question Answering System
This project is an AI-driven web application that enables users to upload PDF documents and interactively ask questions based on the content of those documents. It uses OpenAI's powerful language and embedding models to extract, index, and retrieve relevant information, providing intelligent answers in real-time through a Streamlit interface.

Features
Upload PDF documents for intelligent processing
Ask questions directly based on PDF content
Instant answers powered by OpenAI's GPT and embedding models
Clean and responsive web interface built with Streamlit
Asynchronous backend powered by FastAPI
Persistent indexing for efficient repeated queries

Tech Stack
Frontend: Streamlit
Backend: FastAPI
LLM & Embeddings: OpenAI (GPT-4o-mini, text-embedding-3-small)
PDF Processing: PyMuPDF (fitz)
Vector Indexing: LlamaIndex
Environment Management: Python, pip, dotenv

Installation
Clone the repository
git clone https://github.com/Aarushi163/fullstackpdf-app.git
cd fullstackpdf-app

Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies
pip install -r requirements.txt

Add your OpenAI API key
Create a .env file in the root directory and add:

OPENAI_API_KEY=your_openai_api_key_here
Usage
Start the Backend
uvicorn backend.main:app --host 0.0.0.0 --port 8000
Launch the Frontend
streamlit run app.py
Access the Application
Visit http://localhost:8501 in your browser to use the app.

Project Structure
bash
Copy
Edit
.
├── app.py                  # Streamlit frontend
├── backend/
│   ├── main.py             # FastAPI backend
│   ├── models.py           # Pydantic models
│   └── qa_engine.py        # PDF processing and question answering logic
├── storage/                # Indexed documents are stored here
├── .env                    # OpenAI API key
├── requirements.txt        # Python dependencies
Notes
This application stores the uploaded PDFs and indexes locally in the storage/ directory.
The app uses an in-memory cache for active document indexes and reloads them from disk if necessary.
This project is intended for local or internal use; consider additional security and scaling measures before deploying to production.

Author 
Aarushi Agarwal
