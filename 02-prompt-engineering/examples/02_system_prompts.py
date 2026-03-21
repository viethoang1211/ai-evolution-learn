"""
Module 02 - Example 2: System Prompts and Personas
===================================================
Shows how system prompts dramatically change LLM behavior.

Pain Point: Need consistent behavior across a conversation.
Solution: System prompts define persona and rules.
"""

import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def ask_with_persona(system_prompt: str, user_message: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content


def main():
    user_question = "How do I read a CSV file in Python?"

    personas = {
        "Beginner-Friendly Teacher": """You are a patient programming teacher 
            for absolute beginners. Use simple analogies, avoid jargon, 
            and explain every line of code. Use encouraging language.""",
        "Senior Engineer": """You are a senior software engineer doing a code 
            review. Focus on best practices, error handling, performance, 
            and production readiness. Be direct and technical.""",
        "Security Auditor": """You are a cybersecurity expert reviewing code 
            for vulnerabilities. Focus on input validation, injection risks, 
            data sanitization, and secure coding practices. Flag every 
            potential security issue.""",
        "Minimalist": """You are a developer who believes in extreme brevity. 
            Give the shortest possible answer. No explanations unless asked. 
            Code only.""",
    }

    for persona_name, system_prompt in personas.items():
        print("=" * 60)
        print(f"PERSONA: {persona_name}")
        print("=" * 60)
        response = ask_with_persona(system_prompt, user_question)
        print(f"\n{response}\n")

    print("=" * 60)
    print("LESSON: Same question, 4 completely different answers!")
    print("System prompts control the LLM's 'personality' and focus.")
    print("=" * 60)


if __name__ == "__main__":
    main()
