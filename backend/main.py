from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define a request model for the chatbot
class Message(BaseModel):
    message: str

# Basic route to handle chat messages
@app.post("/chat")
async def chat_response(msg: Message):
    user_message = msg.message.lower()

    # Simple response logic (you can replace this with more complex AI later)
    if "hello" in user_message:
        return {"response": "Hi! How can I assist you today?"}
    elif "bye" in user_message:
        return {"response": "Goodbye! Have a nice day!"}
    else:
        return {"response": "I'm sorry, I don't understand that."}
