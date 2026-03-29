"""
Module 08 - Example 1: Context Window Management
=================================================
Demonstrates practical strategies for managing the context window.

Pain Point: Context windows fill up fast with agent history + tools + docs.
Solution:   Smart summarization, prioritization, and trimming.

Requirements:
    pip install openai tiktoken
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from utils.llm_client import get_client, get_model

client = get_client()


# ============================================
# Token counting (simplified)
# ============================================
def estimate_tokens(text: str) -> int:
    """Rough estimate: ~4 chars per token for English text."""
    return len(text) // 4


# ============================================
# STRATEGY 1: Conversation Summarization
# ============================================
class SummarizingHistory:
    """Keeps recent messages in full, summarizes older ones."""

    def __init__(self, max_recent: int = 4, max_summary_tokens: int = 500):
        self.messages: list[dict] = []
        self.summary: str = ""
        self.max_recent = max_recent
        self.max_summary_tokens = max_summary_tokens

    def add(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        # If too many messages, summarize the oldest ones
        if len(self.messages) > self.max_recent * 2:
            self._summarize_old_messages()

    def _summarize_old_messages(self):
        """Compress old messages into a summary."""
        old = self.messages[: -self.max_recent]
        recent = self.messages[-self.max_recent :]

        old_text = "\n".join(f"{m['role']}: {m['content']}" for m in old)

        # Use LLM to summarize
        response = client.chat.completions.create(
            model=get_model(),
            messages=[
                {
                    "role": "system",
                    "content": "Summarize this conversation history in 2-3 bullet points. "
                    "Preserve key facts, decisions, and any user preferences mentioned.",
                },
                {"role": "user", "content": old_text},
            ],
            max_tokens=200,
        )
        new_summary = response.choices[0].message.content

        if self.summary:
            self.summary = f"{self.summary}\n{new_summary}"
        else:
            self.summary = new_summary

        self.messages = recent
        print(f"  📝 Summarized {len(old)} old messages → {estimate_tokens(self.summary)} tokens")

    def get_context_messages(self) -> list[dict]:
        """Build the messages array with summary + recent."""
        result = []
        if self.summary:
            result.append({
                "role": "system",
                "content": f"## Previous Conversation Summary:\n{self.summary}",
            })
        result.extend(self.messages)
        return result


# ============================================
# STRATEGY 2: Priority-Based Context Selection
# ============================================
class ContextAssembler:
    """Assembles context from multiple sources, prioritized to fit the window."""

    def __init__(self, max_tokens: int = 4000):
        self.max_tokens = max_tokens
        self.layers: list[dict] = []

    def add_layer(self, name: str, content: str, priority: int):
        """Add a context layer. Priority: 1=highest, 4=lowest."""
        tokens = estimate_tokens(content)
        self.layers.append({
            "name": name,
            "content": content,
            "priority": priority,
            "tokens": tokens,
        })

    def assemble(self) -> str:
        """Assemble context, dropping low-priority items if needed."""
        # Sort by priority (highest first)
        sorted_layers = sorted(self.layers, key=lambda x: x["priority"])

        selected = []
        remaining_tokens = self.max_tokens

        for layer in sorted_layers:
            if layer["tokens"] <= remaining_tokens:
                selected.append(layer)
                remaining_tokens -= layer["tokens"]
            else:
                print(f"  ⚠️ Dropped '{layer['name']}' ({layer['tokens']} tokens) — doesn't fit")

        # Build context string
        context_parts = [f"## {l['name']}\n{l['content']}" for l in selected]

        total_tokens = sum(l["tokens"] for l in selected)
        print(f"\n  📊 Context: {total_tokens}/{self.max_tokens} tokens used")
        print(f"  📦 Included: {[l['name'] for l in selected]}")

        return "\n\n".join(context_parts)


# ============================================
# DEMO
# ============================================
def main():
    # ============================================
    # Demo 1: Conversation Summarization
    # ============================================
    print("=" * 60)
    print("DEMO 1: Conversation Summarization")
    print("=" * 60)

    history = SummarizingHistory(max_recent=4)

    # Simulate a long conversation
    conversations = [
        ("user", "My name is Alice and I'm working on a Python web app."),
        ("assistant", "Nice to meet you, Alice! I'd be happy to help with your Python web app."),
        ("user", "I'm using FastAPI with PostgreSQL."),
        ("assistant", "Great stack! FastAPI with PostgreSQL is excellent for modern APIs."),
        ("user", "I need help with database connection pooling."),
        ("assistant", "For connection pooling with PostgreSQL, I recommend using asyncpg with SQLAlchemy."),
        ("user", "What about using SQLModel instead?"),
        ("assistant", "SQLModel is great! It combines SQLAlchemy and Pydantic."),
        ("user", "Now I'm getting a connection timeout error."),
        ("assistant", "Connection timeouts often happen due to pool exhaustion or network issues."),
        ("user", "Can you help me debug this specific error?"),
    ]

    for role, content in conversations:
        history.add(role, content)

    final_messages = history.get_context_messages()
    print(f"\nFinal context has {len(final_messages)} messages:")
    for msg in final_messages:
        role = msg["role"]
        content = msg["content"][:100] + ("..." if len(msg["content"]) > 100 else "")
        print(f"  [{role}]: {content}")

    # ============================================
    # Demo 2: Priority-Based Context Assembly
    # ============================================
    print(f"\n{'='*60}")
    print("DEMO 2: Priority-Based Context Assembly")
    print("=" * 60)

    assembler = ContextAssembler(max_tokens=2000)

    # Add various context sources with priorities
    assembler.add_layer(
        "System Instructions",
        "You are an AI coding assistant. Always use type hints. Follow PEP 8.",
        priority=1,  # Must include
    )

    assembler.add_layer(
        "Current Error",
        """ConnectionError at line 45 in db.py:
        sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) 
        could not connect to server: Connection timed out""",
        priority=1,  # Must include
    )

    assembler.add_layer(
        "Relevant Code",
        """# db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://user:pass@localhost:5432/mydb"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()""",
        priority=2,  # Important
    )

    assembler.add_layer(
        "Documentation Reference",
        """SQLAlchemy Connection Pooling:
        - pool_size: Number of connections to keep (default: 5)
        - max_overflow: Additional connections allowed (default: 10)
        - pool_timeout: Seconds to wait for a connection (default: 30)
        - pool_recycle: Seconds before recycling a connection (default: -1)
        - pool_pre_ping: Test connections before use (default: False)""",
        priority=2,
    )

    assembler.add_layer(
        "User Preferences",
        "User: Alice. Prefers concise answers. Uses FastAPI + PostgreSQL. Experience: intermediate.",
        priority=3,  # Nice to have
    )

    assembler.add_layer(
        "Full Migration History",
        "Alembic migration 001: created users table\n" * 50,  # Very long!
        priority=4,  # Drop first
    )

    context = assembler.assemble()
    print(f"\nAssembled context:\n{context[:500]}...")

    # ============================================
    # Key Lesson
    # ============================================
    print(f"\n{'='*60}")
    print("KEY LESSONS")
    print("=" * 60)
    print("""
    Context Engineering Strategies:
    
    1. 📝 SUMMARIZE: Compress old conversation turns
       - Keep last N messages in full detail
       - Summarize older messages into bullet points
       - ⚡ Saves 60-80% of tokens for long conversations
    
    2. 🎯 PRIORITIZE: Not all context is equal
       - P1: System prompt + current error/query
       - P2: Relevant code + docs
       - P3: User preferences + history summary
       - P4: Background info (drop if needed)
    
    3. 📐 STRUCTURE: Use headers, tags, and formatting
       - Models parse structured text much better
       - XML tags or markdown headers work great
    
    4. 🔄 DYNAMIC: Select context per-query
       - Different queries need different context
       - RAG retrieval is a form of dynamic context selection
    
    This is what separates hobby projects from production AI systems!
    """)


if __name__ == "__main__":
    main()
