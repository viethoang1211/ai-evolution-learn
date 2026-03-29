"""
Module 02 - Example 1: Prompting Techniques Comparison
======================================================
Compare different prompting strategies on the same task
to see how much the technique matters.

Pain Point: Raw prompts give inconsistent results.
Solution: Structured prompting techniques.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from utils.llm_client import get_client, get_model

client = get_client()


def ask(messages: list[dict], temperature: float = 0.0) -> str:
    response = client.chat.completions.create(
        model=get_model(),
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content


def main():
    task = "Is 17077 a prime number?"

    # ============================================
    # Technique 1: Zero-Shot (just ask)
    # ============================================
    print("=" * 60)
    print("TECHNIQUE 1: Zero-Shot")
    print("=" * 60)
    response = ask([{"role": "user", "content": task}])
    print(f"🤖 {response}\n")

    # ============================================
    # Technique 2: Chain-of-Thought
    # ============================================
    print("=" * 60)
    print("TECHNIQUE 2: Chain-of-Thought")
    print("=" * 60)
    response = ask([
        {
            "role": "user",
            "content": f"{task}\n\nThink step by step. Show your reasoning process.",
        }
    ])
    print(f"🤖 {response}\n")

    # ============================================
    # Technique 3: Few-Shot + Chain-of-Thought
    # ============================================
    print("=" * 60)
    print("TECHNIQUE 3: Few-Shot + Chain-of-Thought")
    print("=" * 60)
    response = ask([
        {
            "role": "user",
            "content": """Determine if numbers are prime. Show your work.

Q: Is 29 a prime number?
A: Let me check divisibility by primes up to √29 ≈ 5.4:
   - 29 / 2 = 14.5 (not divisible)
   - 29 / 3 = 9.67 (not divisible)
   - 29 / 5 = 5.8 (not divisible)
   Since no prime up to √29 divides it evenly, 29 IS prime. ✓

Q: Is 51 a prime number?
A: Let me check divisibility by primes up to √51 ≈ 7.1:
   - 51 / 2 = 25.5 (not divisible)
   - 51 / 3 = 17 (divisible!)
   Since 3 divides 51, it is NOT prime. 51 = 3 × 17. ✗

Q: Is 17077 a prime number?
A:""",
        }
    ])
    print(f"🤖 {response}\n")

    # ============================================
    # Technique 4: Role + Chain-of-Thought
    # ============================================
    print("=" * 60)
    print("TECHNIQUE 4: Role + Chain-of-Thought")
    print("=" * 60)
    response = ask([
        {
            "role": "system",
            "content": (
                "You are a mathematician who always verifies answers "
                "by showing complete step-by-step work. Never guess — "
                "always compute."
            ),
        },
        {"role": "user", "content": task},
    ])
    print(f"🤖 {response}\n")

    # ============================================
    # Compare: The right technique matters!
    # ============================================
    print("=" * 60)
    print("LESSON: The same model gives very different results")
    print("depending on HOW you ask. This is Prompt Engineering.")
    print("=" * 60)


if __name__ == "__main__":
    main()
