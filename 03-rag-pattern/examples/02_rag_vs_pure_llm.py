"""
Module 03 - Example 2: RAG vs Pure LLM Comparison
==================================================
Side-by-side comparison showing why RAG matters.

Pain Point: Pure LLM hallucinates about domain-specific knowledge.
Solution:   RAG grounds the LLM in real documents.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from utils.llm_client import get_client, get_model

client = get_client()

# Simulated company-specific information
COMPANY_DOCS = """
TechCorp Internal Engineering Standards (2025):

1. All Python services must use Python 3.12+.
2. Database migrations must use Alembic (not Django migrations).
3. API versioning follows the format /api/v{major}.{minor}/.
4. All services must expose health checks at /healthz and /readyz.
5. Logging must use structured JSON format via structlog.
6. Maximum response time SLA: 200ms for p99 on all API endpoints.
7. Feature flags must go through our internal LaunchDarkly instance.
8. Docker images must be based on python:3.12-slim, not alpine.
9. All secrets must be stored in HashiCorp Vault, never in env vars.
10. CI/CD pipelines must include SAST scanning via Semgrep.
"""


def pure_llm_answer(question: str) -> str:
    """Ask the LLM without any context — it must rely on training data."""
    response = client.chat.completions.create(
        model=get_model(),
        messages=[{"role": "user", "content": question}],
        temperature=0.0,
    )
    return response.choices[0].message.content


def rag_answer(question: str) -> str:
    """Ask the LLM with company documents as context."""
    response = client.chat.completions.create(
        model=get_model(),
        messages=[
            {
                "role": "system",
                "content": f"""Answer based ONLY on this context. If info is not 
in the context, say so.

Context:
{COMPANY_DOCS}""",
            },
            {"role": "user", "content": question},
        ],
        temperature=0.0,
    )
    return response.choices[0].message.content


def main():
    questions = [
        "What Python version should I use for new services?",
        "Where should I store API secrets?",
        "What base Docker image should I use?",
        "What's the p99 latency SLA for our APIs?",
    ]

    for q in questions:
        print("=" * 70)
        print(f"❓ Question: {q}")
        print("-" * 70)
        print(f"🚫 Pure LLM (no context):\n{pure_llm_answer(q)}")
        print()
        print(f"✅ RAG (with company docs):\n{rag_answer(q)}")
        print()

    print("=" * 70)
    print("CONCLUSION: RAG gives company-specific, accurate answers.")
    print("Pure LLM gives generic (often wrong) answers for internal info.")
    print("=" * 70)


if __name__ == "__main__":
    main()
