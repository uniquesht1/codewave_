import os
import httpx
import logging
import traceback
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

app = FastAPI()

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up logging for debugging
logging.basicConfig(level=logging.INFO)

# Define a request model for the chatbot
class Message(BaseModel):
    message: str

# Get TogetherAI API key from the environment variable
TOGETHER_AI_API_KEY = os.getenv("TOGETHER_AI_API_KEY")
TOGETHER_AI_URL = "https://api.together.xyz/v1/completions"

# Function to call TogetherAI API
async def get_ai_response(user_message: str):
    headers = {
        "Authorization": f"Bearer {TOGETHER_AI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",  # Correct model name
        "messages": [
            {
                "role": "system",  # Set up the context and instructions
                "content": (
                    "You are a legal expert with a deep understanding of the law, legal precedents, and regulations. "
                    "You specialize in providing accurate, concise legal advice based on legal documents. "
                    "Please provide responses as if you are a licensed attorney, and cite any relevant laws or cases where applicable."
                )
            },
            {
                "role": "user",  # User's query
                "content": user_message
            }
            ],
            "max_tokens": 512,
            "temperature": 0.5,  # Reduced randomness for more precise legal responses
            "top_p": 0.9,
            "top_k": 50,
            "repetition_penalty": 1.2,  # Increase penalty to avoid repetitive legal jargon
            "stop": ["<|eot_id|>", "<|eom_id|>"],
            "stream": False
        }


    try:
        # Increase the timeout to 30 seconds
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(TOGETHER_AI_URL, json=payload, headers=headers)

        logging.info(f"API Response Headers: {response.headers}")

        # Check for rate limiting (HTTP 429)
        if response.status_code == 429:
            reset_time = int(response.headers.get('x-ratelimit-reset', 60))  # default to 60 seconds
            logging.warning(f"Rate limit exceeded. Retrying after {reset_time} seconds...")
            time.sleep(reset_time)  # Wait for the rate limit to reset
            return await get_ai_response(user_message)  # Retry after waiting

        # Handle a successful response
        if response.status_code == 200:
            data = response.json()
            # Ensure "choices" exists and has content
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

# Basic route to handle chat messages
@app.post("/chat")
async def chat_response(msg: Message):
    user_message = msg.message.lower()

    try:
        ai_response = await get_ai_response(user_message)
        return {"response": ai_response}
    except HTTPException as http_err:
        # Handle specific HTTP-related errors
        return {"response": f"Error: {http_err.detail}"}
    except Exception as e:
        # Catch-all for other errors with logging for debugging
        logging.error(traceback.format_exc())
        return {"response": "Sorry, something went wrong. Please try again later."}


