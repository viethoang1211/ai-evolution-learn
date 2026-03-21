"""
Module 02 - Example 3: Structured Output
=========================================
Shows how to get JSON/structured data from LLMs instead of free text.

Pain Point: Applications need structured data, not prose.
Solution: JSON mode, schema enforcement, output parsing.
"""

import json
import os

from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def extract_structured(text: str) -> dict:
    """Extract structured entities from free text using JSON mode."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """Extract entities from the given text. 
                Return a JSON object with these fields:
                - people: list of {name, role}
                - organizations: list of {name, type}
                - locations: list of {name, type}  
                - dates: list of {value, context}
                - key_facts: list of strings""",
            },
            {"role": "user", "content": text},
        ],
        response_format={"type": "json_object"},
        temperature=0.0,
    )
    return json.loads(response.choices[0].message.content)


def classify_with_schema(text: str) -> dict:
    """Classify text into predefined categories with confidence scores."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """Classify the given text. Return a JSON object with:
                - primary_category: one of [technology, business, science, politics, sports, entertainment]
                - confidence: float 0-1
                - sentiment: one of [positive, negative, neutral, mixed]
                - summary: one sentence summary
                - keywords: list of up to 5 keywords""",
            },
            {"role": "user", "content": text},
        ],
        response_format={"type": "json_object"},
        temperature=0.0,
    )
    return json.loads(response.choices[0].message.content)


def main():
    # ============================================
    # Demo 1: Entity Extraction
    # ============================================
    print("=" * 60)
    print("DEMO 1: Entity Extraction → Structured JSON")
    print("=" * 60)

    article = """
    On March 15, 2025, Anthropic CEO Dario Amodei announced the release 
    of Claude Opus 4 at their headquarters in San Francisco. The new model 
    features extended thinking capabilities and improved agentic workflows. 
    Google's DeepMind team, led by Demis Hassabis in London, responded by 
    showcasing Gemini 2.5's new features the following week.
    """

    result = extract_structured(article)
    print(json.dumps(result, indent=2))

    # ============================================
    # Demo 2: Text Classification
    # ============================================
    print("\n" + "=" * 60)
    print("DEMO 2: Text Classification → Structured JSON")
    print("=" * 60)

    texts = [
        "Apple's stock surged 5% after announcing record iPhone sales in Q4 2025.",
        "The new CRISPR gene therapy showed 95% efficacy in clinical trials.",
        "The team lost their third consecutive match, leaving fans disappointed.",
    ]

    for text in texts:
        print(f"\n📝 Text: {text}")
        result = classify_with_schema(text)
        print(f"📊 Classification: {json.dumps(result, indent=2)}")

    # ============================================
    # Key Lesson
    # ============================================
    print("\n" + "=" * 60)
    print("KEY LESSON")
    print("=" * 60)
    print("""
    Structured output is crucial for building applications:
    
    ✅ Parse-able by downstream code
    ✅ Consistent schema across calls  
    ✅ Can be validated against a schema
    ✅ Enables LLMs to be part of data pipelines
    
    But even with structured output, LLMs still can't:
    ❌ Access real-time data
    ❌ Query your database
    ❌ Take actions in the real world
    
    → This leads us to RAG (Module 03) and Tools (Module 04)
    """)


if __name__ == "__main__":
    main()
