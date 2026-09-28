from __future__ import annotations

from uuid import uuid4
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.app.auth import authenticate_user
from backend.app.graph import graph
from backend.app.prompts import LANGUAGE_NAMES
from backend.app.school_data import LANGUAGES
from backend.app.tools import create_support_request


load_dotenv()

APP_NAME = os.getenv("API_TITLE", "CampusMind AI")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
MAX_MESSAGE_LENGTH = int(os.getenv("MAX_MESSAGE_LENGTH", "2000"))

app = FastAPI(
    title=APP_NAME,
    description="A role-aware, multilingual AI assistant for school communities.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SESSIONS: dict[str, dict] = {}


class LoginRequest(BaseModel):
    email: str
    role: str


class ChatRequest(BaseModel):
    session_id: str
    message: str
    language: str = "English"


class ConfirmRequest(BaseModel):
    session_id: str
    action_type: str


@app.get("/")
def root():
    return {"message": "CampusMind AI backend is running.", "docs": "/docs"}


@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "campusmind-api"}


@app.get("/api/languages")
def languages():
    return {"languages": LANGUAGES}


@app.post("/api/login")
def login(payload: LoginRequest):
    result = authenticate_user(payload.email, payload.role)
    if not result["success"]:
        raise HTTPException(status_code=401, detail=result["error"])

    session_id = str(uuid4())
    user = result["user"]
    SESSIONS[session_id] = {
        "user_id": user["id"],
        "name": user["name"],
        "role": user["role"],
        "history": [],
    }

    return {"success": True, "session_id": session_id, "user": user}


@app.post("/api/chat")
def chat(payload: ChatRequest):
    session = SESSIONS.get(payload.session_id)
    if not session:
        raise HTTPException(status_code=401, detail="Session not found.")

    if payload.language not in LANGUAGE_NAMES:
        raise HTTPException(status_code=400, detail="Unsupported language.")
    if not payload.message.strip():
        raise HTTPException(status_code=422, detail="Message cannot be empty.")
    if len(payload.message) > MAX_MESSAGE_LENGTH:
        raise HTTPException(status_code=422, detail=f"Message must be {MAX_MESSAGE_LENGTH} characters or fewer.")

    state = {
        "query": payload.message,
        "role": session["role"],
        "user_id": session["user_id"],
        "language": payload.language,
        "intent": "",
        "entities": {},
        "answer": "",
        "authorized": False,
        "tool_result": {},
        "conversation_history": session["history"],
        "pending_action": None,
        "security_blocked": False,
    }

    result = graph.invoke(state)

    session["history"].append({"role": "user", "content": payload.message})
    session["history"].append({"role": "assistant", "content": result["answer"]})
    session["history"] = session["history"][-12:]

    return {
        "success": True,
        "answer": result["answer"],
        "intent": result["intent"],
        "authorized": result["authorized"],
        "pending_action": result["pending_action"],
    }


@app.post("/api/support/confirm")
def support_confirm(payload: ConfirmRequest):
    session = SESSIONS.get(payload.session_id)
    if not session:
        raise HTTPException(status_code=401, detail="Session not found.")

    if payload.action_type not in {"teacher", "management"}:
        raise HTTPException(status_code=400, detail="Invalid support type.")

    result = create_support_request(
        session["user_id"],
        session["role"],
        payload.action_type,
        confirmed=True,
    )

    if not result.get("success"):
        raise HTTPException(status_code=403, detail=result["error"])

    return result
