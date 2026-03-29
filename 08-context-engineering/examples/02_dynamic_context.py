"""
Module 08 - Example 2: Dynamic Context Selection
=================================================
Shows how to build a context pipeline that dynamically selects
the right information for each query.

This is how real AI coding assistants work internally.
"""

import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from utils.llm_client import get_client, get_model

client = get_client()


# ============================================
# Simulated codebase and knowledge sources
# ============================================
CODEBASE = {
    "src/auth.py": '''from fastapi import Depends, HTTPException
from jose import jwt
import bcrypt

SECRET_KEY = "change-me-in-production"  # TODO: move to env vars
ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())

def create_token(data: dict) -> str:
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
''',
    "src/models.py": '''from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
''',
    "src/routes.py": '''from fastapi import APIRouter, Depends
from src.models import User
from src.auth import hash_password, create_token

router = APIRouter()

@router.post("/register")
def register(email: str, password: str):
    hashed = hash_password(password)
    # TODO: save to database
    token = create_token({"sub": email})
    return {"token": token}
''',
    "tests/test_auth.py": '''import pytest
from src.auth import hash_password, verify_password

def test_hash_password():
    hashed = hash_password("test123")
    assert hashed != "test123"
    assert verify_password("test123", hashed)
''',
}

DOCS = {
    "api_docs": "API endpoints: POST /register, POST /login, GET /profile. All require JSON body.",
    "deployment_guide": "Deploy with Docker. Use docker-compose for local dev. CI/CD via GitHub Actions.",
    "security_policy": "All secrets via env vars. Rotate JWT keys monthly. Rate limit auth endpoints.",
}

ERROR_LOGS = [
    "[2025-03-20 10:15:23] ERROR: JWT decode failed - token expired for user alice@example.com",
    "[2025-03-20 10:16:01] WARNING: Rate limit exceeded from IP 192.168.1.100",
    "[2025-03-20 10:16:45] ERROR: Database connection pool exhausted (max: 5, waiting: 12)",
]


# ============================================
# CONTEXT SELECTION ENGINE
# ============================================
def classify_query(query: str) -> dict:
    """Use LLM to classify what context a query needs."""
    response = client.chat.completions.create(
        model=get_model(),
        messages=[
            {
                "role": "system",
                "content": """Classify this developer query. Return JSON with:
{
    "intent": "debug|feature|review|question|deploy",
    "needs_code": true/false,
    "relevant_files": ["list of likely relevant file paths"],
    "needs_docs": true/false,
    "needs_logs": true/false,
    "keywords": ["key", "terms"]
}""",
            },
            {"role": "user", "content": query},
        ],
        response_format={"type": "json_object"},
        temperature=0.0,
    )
    return json.loads(response.choices[0].message.content)


def select_context(query: str, max_tokens: int = 3000) -> str:
    """Dynamically select the right context for this specific query."""
    print(f"\n🔍 Analyzing query: '{query}'")

    # Step 1: Classify the query
    classification = classify_query(query)
    print(f"📋 Classification: {json.dumps(classification, indent=2)}")

    # Step 2: Select context based on classification
    context_parts = []
    token_budget = max_tokens

    # Always include: system instructions
    system_ctx = "You are an expert Python developer helping with a FastAPI project."
    context_parts.append(f"## Instructions\n{system_ctx}")
    token_budget -= len(system_ctx) // 4

    # Include code files if needed
    if classification.get("needs_code"):
        relevant_files = classification.get("relevant_files", [])
        for file_path in relevant_files:
            # Find matching files (fuzzy match)
            for actual_path, content in CODEBASE.items():
                if any(part in actual_path for part in file_path.split("/")):
                    file_tokens = len(content) // 4
                    if file_tokens <= token_budget:
                        context_parts.append(f"## File: {actual_path}\n```python\n{content}\n```")
                        token_budget -= file_tokens
                        print(f"  📄 Included: {actual_path} ({file_tokens} tokens)")

    # Include docs if needed
    if classification.get("needs_docs"):
        for doc_name, doc_content in DOCS.items():
            doc_tokens = len(doc_content) // 4
            if doc_tokens <= token_budget:
                context_parts.append(f"## Documentation: {doc_name}\n{doc_content}")
                token_budget -= doc_tokens
                print(f"  📚 Included: {doc_name} ({doc_tokens} tokens)")

    # Include error logs if debugging
    if classification.get("needs_logs") or classification.get("intent") == "debug":
        logs = "\n".join(ERROR_LOGS)
        log_tokens = len(logs) // 4
        if log_tokens <= token_budget:
            context_parts.append(f"## Recent Error Logs\n{logs}")
            token_budget -= log_tokens
            print(f"  🔴 Included: error logs ({log_tokens} tokens)")

    total_used = max_tokens - token_budget
    print(f"\n  📊 Context: {total_used}/{max_tokens} tokens used")

    return "\n\n".join(context_parts)


def answer_with_context(query: str) -> str:
    """Full pipeline: classify → select context → answer."""
    context = select_context(query)

    response = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": query},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content


# ============================================
# DEMO
# ============================================
def main():
    print("=" * 60)
    print("DYNAMIC CONTEXT SELECTION DEMO")
    print("=" * 60)

    queries = [
        # Debug query → needs code + logs
        "Why am I seeing 'Database connection pool exhausted' errors?",

        # Feature query → needs code + docs
        "How do I add a /login endpoint to the API?",

        # Security review → needs code + security docs
        "Review the authentication code for security issues.",

        # Deployment query → needs docs only
        "How do I deploy this to production?",
    ]

    for query in queries:
        print(f"\n{'='*60}")
        answer = answer_with_context(query)
        print(f"\n🤖 Answer:\n{answer[:500]}...")

    print(f"\n{'='*60}")
    print("KEY INSIGHT: Different Queries = Different Context")
    print("=" * 60)
    print("""
    Notice how each query got DIFFERENT context:
    
    🐛 Debug query       → code files + error logs
    ✨ Feature query      → code files + API docs
    🔒 Security review   → code files + security policy
    🚀 Deployment query  → deployment docs (no code needed!)
    
    This is CONTEXT ENGINEERING in action:
    ✅ Each query gets only relevant information
    ✅ Token budget is used efficiently
    ✅ Model gets focused, high-signal context
    ✅ Results are more accurate and relevant
    
    This is exactly what tools like GitHub Copilot do —
    they analyze your current file, cursor position, open tabs,
    and recent edits to select the right context for each completion.
    """)


if __name__ == "__main__":
    main()
