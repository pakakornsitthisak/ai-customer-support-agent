from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.llm import generate_response
from app.memory import clear_history


app = FastAPI(
    title="AI Customer Support Agent",
    description="An AI customer support agent using Ollama and tool calling.",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


class ChatResponse(BaseModel):
    answer: str


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    answer = generate_response(
        message=request.message,
        session_id=request.session_id,
    )

    return ChatResponse(
        answer=answer,
    )


@app.delete("/sessions/{session_id}")
def delete_session(session_id: str):
    clear_history(session_id)

    return {
        "session_id": session_id,
        "status": "cleared",
    }
