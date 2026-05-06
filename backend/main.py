import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from rag import initialize_components, generate_answer
from rbac import VALID_ROLES


# ── LOAD ENV VARIABLES ────────────────────────────────────
load_dotenv(dotenv_path="../.env")


# ── FAKE USER DATABASE (replace with real DB later) ────────
USERS = {
    "alice":   {"password": "alice123",   "role": "finance"},
    "bob":     {"password": "bob123",     "role": "hr"},
    "charlie": {"password": "charlie123", "role": "marketing"},
    "diana":   {"password": "diana123",   "role": "engineering"},
    "eve":     {"password": "eve123",     "role": "c_level"},
    "frank":   {"password": "frank123",   "role": "employee"},
}


# ── FASTAPI LIFESPAN HANDLER (modern replacement of startup event) ──
@asynccontextmanager
async def lifespan(app: FastAPI):

    print("\n🚀 Initializing RAG components...")
    initialize_components()
    print("✅ RAG components ready.\n")

    yield

    print("🛑 Shutting down FinSolve Chatbot API...")


# ── APP INITIALIZATION ────────────────────────────────────
app = FastAPI(
    title="FinSolve Chatbot API",
    description="Secure RBAC-enabled RAG internal assistant",
    version="2.0.0",
    lifespan=lifespan
)


# ── ENABLE CORS ───────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── REQUEST MODELS ────────────────────────────────────────
class LoginRequest(BaseModel):
    username: str
    password: str


class ChatRequest(BaseModel):
    username: str
    question: str


# ── RESPONSE MODELS ───────────────────────────────────────
class LoginResponse(BaseModel):
    username: str
    role: str
    message: str


class ChatResponse(BaseModel):
    answer: str
    sources: list
    role: str


# ── ROOT ENDPOINT ─────────────────────────────────────────
@app.get("/")
def root():
    return {"message": "FinSolve Chatbot API is running 🚀"}


# ── LOGIN ENDPOINT ────────────────────────────────────────
@app.post("/login", response_model=LoginResponse)
def login(request: LoginRequest):

    username = request.username.lower().strip()
    password = request.password.strip()

    if username not in USERS:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if USERS[username]["password"] != password:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    role = USERS[username]["role"]

    return LoginResponse(
        username=username,
        role=role,
        message=f"Welcome {username}! Logged in as {role}."
    )


# ── CHAT ENDPOINT (RBAC ENFORCED SECURELY) ─────────────────
@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    question = request.question.strip()
    username = request.username.lower().strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    if username not in USERS:
        raise HTTPException(
            status_code=403,
            detail="Invalid user session"
        )

    role = USERS[username]["role"]

    if role not in VALID_ROLES:
        raise HTTPException(
            status_code=403,
            detail=f"Unauthorized role: {role}"
        )

    try:

        answer, sources = generate_answer(
            query=question,
            role=role
        )

        return ChatResponse(
            answer=answer,
            sources=sources,
            role=role
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"RAG processing error: {str(e)}"
        )


# ── AVAILABLE ROLES ENDPOINT ──────────────────────────────
@app.get("/roles")
def get_roles():
    return {"roles": VALID_ROLES}