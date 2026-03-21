"""
Module 01 - Example 2: LLM Statelessness Demo
===============================================
Demonstrates that LLMs have NO memory between API calls.
This is the #1 pain point that drives the need for conversation management.

Pain Point: Each call is independent — the model forgets everything.
Solution Preview: Message history (Module 02), RAG (Module 03)
"""

import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def single_call(prompt: str) -> str:
    """Each call is completely independent."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
    )
    return response.choices[0].message.content


def conversation_with_history(messages: list[dict]) -> str:
    """Pass the full conversation history to simulate memory."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.0,
    )
    return response.choices[0].message.content


def main():
    # ============================================
    # DEMO 1: Statelessness — The Problem
    # ============================================
    print("=" * 60)
    print("DEMO 1: Statelessness — Each call is independent")
    print("=" * 60)

    print("\n📝 Call 1: 'My name is Alice and I love Python.'")
    response1 = single_call("My name is Alice and I love Python.")
    print(f"🤖 Response: {response1}")

    print("\n📝 Call 2: 'What is my name and what do I love?'")
    response2 = single_call("What is my name and what do I love?")
    print(f"🤖 Response: {response2}")
    print("\n⚠️  Notice: The model has NO IDEA who you are in Call 2!")

    # ============================================
    # DEMO 2: Manual Memory — The Workaround
    # ============================================
    print("\n" + "=" * 60)
    print("DEMO 2: Manual Memory — Passing conversation history")
    print("=" * 60)

    messages = [
        {"role": "user", "content": "My name is Alice and I love Python."},
        {
            "role": "assistant",
            "content": "Nice to meet you, Alice! Python is a great language.",
        },
        {"role": "user", "content": "What is my name and what do I love?"},
    ]

    print("\n📝 Sending full conversation history...")
    for msg in messages:
        print(f"   [{msg['role']}]: {msg['content']}")

    response3 = conversation_with_history(messages)
    print(f"\n🤖 Response: {response3}")
    print("\n✅ Now the model 'remembers' because we sent the full history!")

    # ============================================
    # DEMO 3: The Cost of "Memory"
    # ============================================
    print("\n" + "=" * 60)
    print("DEMO 3: The Cost of Simulated Memory")
    print("=" * 60)
    print("""
    ┌─────────────────────────────────────────────┐
    │  Turn 1:  Send 1 message      → ~50 tokens  │
    │  Turn 2:  Send 2 messages     → ~100 tokens  │
    │  Turn 3:  Send 3 messages     → ~150 tokens  │
    │  ...                                         │
    │  Turn 100: Send 100 messages  → ~5000 tokens  │
    └─────────────────────────────────────────────┘
    
    Problem: Token usage grows linearly with conversation length!
    Cost grows quadratically due to attention mechanism.
    
    This creates the need for:
    → Summarization strategies
    → RAG (Retrieval-Augmented Generation) — Module 03
    → Context Engineering — Module 08
    """)


if __name__ == "__main__":
    main()
