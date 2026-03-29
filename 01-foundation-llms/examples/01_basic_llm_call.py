"""
Module 01 - Example 1: Basic LLM API Call
==========================================
Demonstrates the simplest interaction with an LLM via API.

Pain Point Illustrated: None yet — this is our baseline.

Requirements:
    pip install openai
    export OPENAI_API_KEY="your-key-here"
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from utils.llm_client import get_client, get_model

client = get_client()


def basic_completion(prompt: str) -> str:
    """The simplest possible LLM call — text in, text out."""
    response = client.chat.completions.create(
        model=get_model(),
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500,
    )
    return response.choices[0].message.content


def main():
    # Simple question answering
    print("=" * 60)
    print("EXAMPLE 1: Basic Question Answering")
    print("=" * 60)

    questions = [
        "What is the capital of France?",
        "Explain quantum computing in one sentence.",
        "Write a Python function to check if a number is prime.",
    ]

    for question in questions:
        print(f"\n📝 Question: {question}")
        answer = basic_completion(question)
        print(f"🤖 Answer: {answer}")
        print("-" * 40)


if __name__ == "__main__":
    main()
