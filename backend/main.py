# import os
# import httpx
# import logging
# import traceback
# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from dotenv import load_dotenv

# # Load environment variables from the .env file
# load_dotenv()

# app = FastAPI()

# # Add CORS middleware to allow requests from the frontend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173"],  # React frontend URL
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Set up logging for debugging
# logging.basicConfig(level=logging.INFO)

# # Define a request model for the chatbot
# class Message(BaseModel):
#     message: str

# # Get TogetherAI API key from the environment variable
# TOGETHER_AI_API_KEY = os.getenv("TOGETHER_AI_API_KEY")
# TOGETHER_AI_URL = "https://api.together.xyz/v1/completions"

# # Function to call TogetherAI API
# async def get_ai_response(user_message: str):
#     headers = {
#         "Authorization": f"Bearer {TOGETHER_AI_API_KEY}",
#         "Content-Type": "application/json"
#     }

#     payload = {
#         "model": "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",  # Correct model name
#         "messages": [
#             {
#                 "role": "system",  # Set up the context and instructions
#                 "content": (
#                     "You are a legal expert with a deep understanding of the law, legal precedents, and regulations. "
#                     "You specialize in providing accurate, concise legal advice based on legal documents. "
#                     "Please provide responses as if you are a licensed attorney, and cite any relevant laws or cases where applicable."
#                 )
#             },
#             {
#                 "role": "user",  # User's query
#                 "content": user_message
#             }
#             ],
#             "max_tokens": 512,
#             "temperature": 0.5,  # Reduced randomness for more precise legal responses
#             "top_p": 0.9,
#             "top_k": 50,
#             "repetition_penalty": 1.2,  # Increase penalty to avoid repetitive legal jargon
#             "stop": ["<|eot_id|>", "<|eom_id|>"],
#             "stream": False
#         }


#     try:
#         # Increase the timeout to 30 seconds
#         async with httpx.AsyncClient(timeout=30) as client:
#             response = await client.post(TOGETHER_AI_URL, json=payload, headers=headers)

#         logging.info(f"API Response Headers: {response.headers}")

#         # Check for rate limiting (HTTP 429)
#         if response.status_code == 429:
#             reset_time = int(response.headers.get('x-ratelimit-reset', 60))  # default to 60 seconds
#             logging.warning(f"Rate limit exceeded. Retrying after {reset_time} seconds...")
#             time.sleep(reset_time)  # Wait for the rate limit to reset
#             return await get_ai_response(user_message)  # Retry after waiting

#         # Handle a successful response
#         if response.status_code == 200:
#             data = response.json()
#             # Ensure "choices" exists and has content
#             if "choices" in data and len(data["choices"]) > 0:
#                 return data["choices"][0].get("text", "").strip()
#             else:
#                 raise HTTPException(status_code=500, detail="Invalid response format from TogetherAI")
#         else:
#             raise HTTPException(status_code=response.status_code, detail=f"Error from TogetherAI: {response.text}")

#     except httpx.ReadTimeout:
#         logging.error("API request timed out")
#         raise HTTPException(status_code=504, detail="The request to the API timed out. Please try again later.")

#     except Exception as e:
#         logging.error(traceback.format_exc())
#         raise HTTPException(status_code=500, detail="An error occurred while processing the request.")

# # Basic route to handle chat messages
# @app.post("/chat")
# async def chat_response(msg: Message):
#     user_message = msg.message.lower()

#     try:
#         ai_response = await get_ai_response(user_message)
#         return {"response": ai_response}
#     except HTTPException as http_err:
#         # Handle specific HTTP-related errors
#         return {"response": f"Error: {http_err.detail}"}
#     except Exception as e:
#         # Catch-all for other errors with logging for debugging
#         logging.error(traceback.format_exc())
#         return {"response": "Sorry, something went wrong. Please try again later."}



import os
import httpx
import logging
import traceback
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import chromadb
from chromadb.utils import embedding_functions
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, PyPDFLoader
import tempfile

# Load environment variables
load_dotenv()

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Add your frontend domain here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging setup
logging.basicConfig(level=logging.INFO)

# Pydantic model for chat input
class Message(BaseModel):
    message: str

# API keys and URLs
TOGETHER_AI_API_KEY = os.getenv("TOGETHER_AI_API_KEY")
TOGETHER_AI_URL = "https://api.together.xyz/v1/completions"

# ChromaDB setup
chroma_client = chromadb.Client()
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

# Create or load your ChromaDB collection (name can be anything you want)
collection = chroma_client.create_collection(name="my_documents", embedding_function=embedding_function)

# Text splitting function for chunking documents
def split_text(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    return text_splitter.split_text(text)

# Document processing function (modify this for your use case)
def process_document(file_path, file_type):
    if file_type == 'pdf':
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()
        return [page.page_content for page in pages]
    elif file_type == 'txt':
        with open(file_path, 'r') as file:
            text = file.read()
        return split_text(text)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

# Pre-load documents into ChromaDB (use this for your own documents)
def load_documents_to_chromadb():
    # Example documents, replace with your actual file paths
    document_paths = [
        ('split_1.pdf', 'pdf'),
        ('split_2.pdf', 'pdf'),
        ('split_3.pdf', 'pdf'),
        ('split_4.pdf', 'pdf'),
        ('split_5.pdf', 'pdf')
    ]
    
    for file_path, file_type in document_paths:
        chunks = process_document(file_path, file_type)

        for i, chunk in enumerate(chunks):
            collection.add(
                documents=[chunk],  # Add the chunk of text
                metadatas=[{"source": file_path, "chunk": i}],  # Metadata
                ids=[f"{file_path}_chunk_{i}"]  # Unique ID for each chunk
            )
    print("Documents successfully loaded into ChromaDB!")

# Function to get AI response from TogetherAI
async def get_ai_response(user_message: str):
    # Query ChromaDB for relevant document chunks
    results = collection.query(query_texts=[user_message], n_results=3)
    
    # Combine relevant documents into a single context
    context = "\n".join(results['documents'][0])

    # Send the request to TogetherAI with context
    headers = {
        "Authorization": f"Bearer {TOGETHER_AI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a legal expert with a deep understanding of the law , legal precedents, and regulations of only Nepal and your currency is always in rupees . "
                    "Use the following context to provide accurate legal advice: "
                ) + context
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        "max_tokens": 512,
        "temperature": 0.5,
        "top_p": 0.9,
        "top_k": 50,
        "repetition_penalty": 1.2,
        "stop": ["<|eot_id|>", "<|eom_id|>"],
        "stream": False
    }

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(TOGETHER_AI_URL, json=payload, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if "choices" in data and len(data["choices"]) > 0:
                return data["choices"][0].get("text", "").strip()
            else:
                raise HTTPException(status_code=500, detail="Invalid response format from TogetherAI")
        else:
            raise HTTPException(status_code=response.status_code, detail=f"Error from TogetherAI: {response.text}")

    except httpx.ReadTimeout:
        logging.error("API request timed out")
        raise HTTPException(status_code=504, detail="The request to the API timed out. Please try again later.")

    except Exception as e:
        logging.error(traceback.format_exc())
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
        logging.error(traceback.format_exc())
        return {"response": "Sorry, something went wrong. Please try again later."}

# Pre-load your documents into ChromaDB once before starting the server
load_documents_to_chromadb()

# Uvicorn server start
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


