"""
Module 01 - Example 3: Hallucination Demo
==========================================
Demonstrates that LLMs can confidently generate false information.

Pain Point: LLMs don't "know" what they don't know.
Solution Preview: RAG (Module 03), Tool Use (Module 04)
"""

import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def ask_llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return response.choices[0].message.content


def main():
    print("=" * 60)
    print("HALLUCINATION DEMO: LLMs Confidently Make Things Up")
    print("=" * 60)

    # Test 1: Ask about a fake paper
    print("\n📝 Test 1: Ask about a non-existent research paper")
    print("-" * 40)
    response = ask_llm(
        "Summarize the key findings of the research paper "
        "'Quantum Neural Oscillations in Deep Learning' "
        "by Dr. James Richardson, published in Nature 2024."
    )
    print(f"🤖 Response:\n{response}")
    print("\n⚠️  This paper does NOT exist! But the model described it confidently.")

    # Test 2: Ask about fake historical events
    print("\n📝 Test 2: Ask about a non-existent historical event")
    print("-" * 40)
    response = ask_llm(
        "Tell me about the Great Server Migration of 2019, "
        "when all of Europe's cloud infrastructure was moved from "
        "AWS to a European sovereign cloud provider."
    )
    print(f"🤖 Response:\n{response}")
    print("\n⚠️  This event never happened!")

    # Test 3: Real-time information
    print("\n📝 Test 3: Ask for real-time information")
    print("-" * 40)
    response = ask_llm("What is the current price of Bitcoin right now?")
    print(f"🤖 Response:\n{response}")
    print("\n⚠️  The model cannot access real-time data!")

    # The solution preview
    print("\n" + "=" * 60)
    print("THE SOLUTION: Ground LLMs in Facts")
    print("=" * 60)
    print("""
    These problems lead to two major innovations:
    
    1. RAG (Retrieval-Augmented Generation) — Module 03
       → Feed real documents to the LLM so it answers from facts
       
    2. Tool Use / Function Calling — Module 04
       → Let the LLM call APIs for real-time data
       
    3. Agentic AI — Module 06
       → Let the LLM decide WHEN to search vs. answer from knowledge
    """)


if __name__ == "__main__":
    main()
