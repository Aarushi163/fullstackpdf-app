# qa_engine.py
import os
from pathlib import Path
import fitz  # PyMuPDF
from dotenv import load_dotenv

from llama_index.core import VectorStoreIndex, Document, StorageContext, load_index_from_storage
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import SentenceSplitter

# Load API key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise EnvironmentError("❌ OPENAI_API_KEY not found in .env file")

# Storage path
STORAGE = Path("storage")
STORAGE.mkdir(exist_ok=True)
INDEX_DIR = STORAGE / "indexes"
INDEX_DIR.mkdir(exist_ok=True)

INDEXES = {}

# Initialize chunk parser
parser = SentenceSplitter(chunk_size=512, chunk_overlap=50)

# Use faster OpenAI embedding model
embed_model = OpenAIEmbedding(model="text-embedding-3-small", api_key=OPENAI_API_KEY)
llm = OpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)

def save_pdf(file_bytes, filename):
    filepath = STORAGE / filename
    with open(filepath, "wb") as f:
        f.write(file_bytes)
    return filepath

def extract_text(filepath):
    doc = fitz.open(filepath)
    return "\n".join(page.get_text() for page in doc)

def process_pdf_and_build_index_background(doc_id, file_bytes):
    try:
        filepath = save_pdf(file_bytes, f"{doc_id}.pdf")
        text = extract_text(filepath)
        if not text.strip():
            print(f"[INDEX] PDF {doc_id} has no extractable text.")
            return

        document = Document(text=text, metadata={"doc_id": doc_id})
        nodes = parser.get_nodes_from_documents([document])

        index = VectorStoreIndex(nodes, embed_model=embed_model, llm=llm)
        index.storage_context.persist(persist_dir=str(INDEX_DIR / doc_id))
        INDEXES[doc_id] = index
        print(f"[INDEX] Completed for doc_id={doc_id}")
    except Exception as e:
        print(f"[INDEX ERROR] {e}")

def is_index_ready(doc_id):
    if doc_id in INDEXES:
        return True
    index_path = INDEX_DIR / doc_id
    if index_path.exists():
        try:
            storage_context = StorageContext.from_defaults(persist_dir=str(index_path))
            index = load_index_from_storage(storage_context)
            INDEXES[doc_id] = index
            return True
        except:
            return False
    return False

def answer_question(doc_id, question):
    index = INDEXES.get(doc_id)
    if not index:
        raise ValueError(f"No index found for doc_id: {doc_id}")
    query_engine = index.as_query_engine()
    response = query_engine.query(question)
    return str(response)