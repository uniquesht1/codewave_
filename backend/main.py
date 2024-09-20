
import os
import httpx
import logging
import traceback
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import sqlite3
import numpy as np
from chromadb.utils import embedding_functions
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
import chromadb
from pathlib import Path

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Add your frontend domain here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic model for chat input
class Message(BaseModel):
    message: str

# Embedding function setup
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

# Initialize ChromaDB client
chroma_client = chromadb.Client()

# Create or get the collection
collection = chroma_client.create_collection(name="legal_documents")

# SQLite Database setup
def create_db():
    conn = sqlite3.connect('embeddings.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS embeddings (
        id TEXT PRIMARY KEY,
        document TEXT,
        metadata TEXT,
        embedding BLOB
    )
    ''')
    conn.commit()
    conn.close()
    logger.info("SQLite database initialized")

# Text splitting function for chunking documents
def split_text(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    return text_splitter.split_text(text)

# Document processing function
def process_document(file_path, file_type):
    if file_type == 'pdf':
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()
        return [page.page_content for page in pages]
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

# Function to check if a document has already been processed
def document_exists_in_db(file_path):
    conn = sqlite3.connect('embeddings.db')
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM embeddings WHERE id LIKE ?', (f"{file_path}%",))
    count = c.fetchone()[0]
    conn.close()
    return count > 0

# Function to save embeddings to SQLite database
def save_embedding_to_sqlite(doc_id, chunk, metadata, embedding):
    conn = sqlite3.connect('embeddings.db')
    c = conn.cursor()
    embedding_array = np.array(embedding, dtype=np.float32)
    c.execute(
        'INSERT OR REPLACE INTO embeddings (id, document, metadata, embedding) VALUES (?, ?, ?, ?)',
        (doc_id, chunk, str(metadata), embedding_array.tobytes())
    )
    conn.commit()
    conn.close()

# Pre-load documents into SQLite and ChromaDB
def load_documents():
    document_paths = [
        ('split_1.pdf', 'pdf'),
        ('split_2.pdf', 'pdf'),
        ('split_3.pdf', 'pdf'),
        ('split_4.pdf', 'pdf'),
        ('split_5.pdf', 'pdf') # Add more document paths as needed
    ]
    
    for file_path, file_type in document_paths:
        if document_exists_in_db(file_path):
            logger.info(f"Skipping {file_path} as it's already in the database")
            continue

        logger.info(f"Processing {file_path}")
        chunks = process_document(file_path, file_type)

        for i, chunk in enumerate(chunks):
            embedding = embedding_function([chunk])
            doc_id = f"{file_path}_chunk_{i}"
            metadata = {"source": file_path, "chunk": i}
            save_embedding_to_sqlite(doc_id, chunk, metadata, embedding[0])
        
        logger.info(f"Finished processing {file_path}")

# Function to load embeddings from SQLite and add to ChromaDB
def load_embeddings_to_chromadb():
    if collection.count() > 0:
        logger.info("ChromaDB collection already populated, skipping loading")
        return

    conn = sqlite3.connect('embeddings.db')
    c = conn.cursor()
    c.execute('SELECT id, document, metadata, embedding FROM embeddings')
    rows = c.fetchall()
    conn.close()

    for row in rows:
        doc_id, document, metadata, embedding_blob = row
        embedding = np.frombuffer(embedding_blob, dtype=np.float32)
        
        # Add embeddings to ChromaDB
        collection.add(
            documents=[document],
            metadatas=[eval(metadata)],  # Convert string metadata back to dict
            ids=[doc_id],
            embeddings=[embedding.tolist()]  # Convert numpy array to list
        )
    
    logger.info(f"Loaded {len(rows)} embeddings into ChromaDB")

# Function to get AI response from TogetherAI
async def get_ai_response(user_message: str):
    # Query ChromaDB for relevant document chunks
    results = collection.query(query_texts=[user_message], n_results=3)
    
    # Combine relevant documents into a single context
    context = "\n".join(results['documents'][0])

    # Send the request to TogetherAI with context
    headers = {
        "Authorization": f"Bearer {os.getenv('TOGETHER_AI_API_KEY')}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a legal expert with a deep understanding of the law, legal precedents, and regulations of only Nepal and your currency is always in rupees. "
                    "Use the following context to provide accurate legal advice: "
                    "For any list or series of points, use bullet points. Keep the answer to under 5 sentences if possible."
                ) + context
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        "max_tokens": 300,
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 50,
        "repetition_penalty": 1.2,
        "stop": ["<|eot_id|>", "<|eom_id|>"],
        "stream": False
    }

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(os.getenv('TOGETHER_AI_URL'), json=payload, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if "choices" in data and len(data["choices"]) > 0:
                return data["choices"][0].get("text", "").strip()
            else:
                raise HTTPException(status_code=500, detail="Invalid response format from TogetherAI")
        else:
            raise HTTPException(status_code=response.status_code, detail=f"Error from TogetherAI: {response.text}")

    except httpx.ReadTimeout:
        logger.error("API request timed out")
        raise HTTPException(status_code=504, detail="The request to the API timed out. Please try again later.")

    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")

# Chat endpoint for querying the chatbot
@app.post("/chat")
async def chat_response(msg: Message):
    user_message = msg.message.lower()

    try:
        ai_response = await get_ai_response(user_message)
        return {"response": ai_response}
    except HTTPException as http_err:
        return {"response": f"Error: {http_err.detail}"}
    except Exception as e:
        logger.error(traceback.format_exc())
        return {"response": "Sorry, something went wrong. Please try again later."}

# Initialize the database and load documents
@app.on_event("startup")
async def startup_event():
    create_db()
    load_documents()
    load_embeddings_to_chromadb()

# Uvicorn server start
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)