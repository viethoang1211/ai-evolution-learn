"""
Module 05 - Example 2: ReAct with Error Recovery
=================================================
Shows how ReAct agents can handle failures and adapt their strategy.

Pain Point: Simple function calling fails silently.
Solution:   ReAct agents reason about errors and try alternatives.
"""

import json
import sys
import os
import random

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from utils.llm_client import get_client, get_model

client = get_client()


# ============================================
# UNRELIABLE TOOLS — simulate real-world failures
# ============================================
call_count = 0


def unreliable_api(endpoint: str) -> str:
    """Simulates an API that sometimes fails (like real APIs do)."""
    global call_count
    call_count += 1

    # Fail 50% of the time
    if random.random() < 0.5:
        return json.dumps({"error": "503 Service Unavailable — API is temporarily down"})

    data = {
        "weather": '{"city": "Tokyo", "temp_c": 22, "condition": "Sunny"}',
        "stock": '{"symbol": "AAPL", "price": 195.50, "change": "+2.3%"}',
        "news": '{"headline": "AI adoption grows 40% in enterprise", "source": "TechCrunch"}',
    }
    for key, value in data.items():
        if key in endpoint.lower():
            return value
    return json.dumps({"error": f"Unknown endpoint: {endpoint}"})


def cache_lookup(key: str) -> str:
    """A cache that might have stale data — fallback option."""
    cache = {
        "weather:tokyo": '{"city": "Tokyo", "temp_c": 20, "condition": "Cloudy", "cached": true, "cache_age": "2 hours"}',
        "stock:aapl": '{"symbol": "AAPL", "price": 193.20, "change": "+1.8%", "cached": true, "cache_age": "1 hour"}',
    }
    return cache.get(key, json.dumps({"error": "Cache miss — no cached data available"}))


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "unreliable_api",
            "description": "Call an external API endpoint. May fail sometimes (real-world simulation). Endpoints: 'weather', 'stock', 'news'",
            "parameters": {
                "type": "object",
                "properties": {
                    "endpoint": {"type": "string", "description": "API endpoint name like 'weather', 'stock', 'news'"}
                },
                "required": ["endpoint"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "cache_lookup",
            "description": "Look up cached data. Might be stale but more reliable. Keys: 'weather:tokyo', 'stock:aapl'",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {"type": "string", "description": "Cache key like 'weather:tokyo'"}
                },
                "required": ["key"],
            },
        },
    },
]

TOOL_MAP = {
    "unreliable_api": unreliable_api,
    "cache_lookup": cache_lookup,
}


def react_with_recovery(question: str, max_steps: int = 8) -> str:
    """ReAct agent that handles tool failures gracefully."""
    print(f"\n{'='*60}")
    print(f"❓ Question: {question}")
    print(f"{'='*60}")

    messages = [
        {
            "role": "system",
            "content": """You are a resilient ReAct agent. You solve problems step by step.

Available tools:
- unreliable_api(endpoint): Call an external API. Sometimes fails with 503 errors.
- cache_lookup(key): Fallback cache. More reliable but may have stale data.

Strategy for handling failures:
1. Try the API first for fresh data
2. If it fails, RETRY once
3. If it fails again, fall back to the cache
4. Always tell the user if you're using cached (potentially stale) data
5. Never pretend you have data you don't have

Think through each step carefully."""
        },
        {"role": "user", "content": question},
    ]

    for step in range(max_steps):
        print(f"\n--- Step {step + 1} ---")

        response = client.chat.completions.create(
            model=get_model(),
            messages=messages,
            tools=TOOLS,
        )
        message = response.choices[0].message

        if message.content:
            print(f"💭 Thought: {message.content}")

        if message.tool_calls:
            messages.append(message)
            for tool_call in message.tool_calls:
                func_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                print(f"🔧 Action: {func_name}({args})")

                result = TOOL_MAP[func_name](**args)
                print(f"👁️ Observation: {result}")

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                })
        else:
            print(f"\n✅ Final Answer: {message.content}")
            return message.content

    return "Max steps reached."


def main():
    global call_count

    print("=" * 60)
    print("ReAct WITH ERROR RECOVERY DEMO")
    print("=" * 60)
    print("(Tools randomly fail ~50% of the time — watch the agent adapt!)\n")

    random.seed(42)  # For reproducibility

    # Query that requires handling unreliable APIs
    call_count = 0
    react_with_recovery("What's the current weather in Tokyo?")
    print(f"\n📊 Total API calls made: {call_count}")

    # Another query
    call_count = 0
    react_with_recovery("What's Apple's current stock price?")
    print(f"\n📊 Total API calls made: {call_count}")

    print("\n" + "=" * 60)
    print("KEY INSIGHT: Error Recovery Strategy")
    print("=" * 60)
    print("""
    The ReAct agent demonstrated:
    
    1. 🔄 RETRY: When API failed, it tried again
    2. 🔀 FALLBACK: When retries failed, it used the cache
    3. 📢 TRANSPARENCY: Told the user when data was cached/stale
    4. 🧠 REASONING: Made decisions based on each observation
    
    This is impossible with simple function calling!
    Simple function calling would just fail and return an error.
    
    → This resilience pattern is fundamental to Agentic AI (Module 06)
    """)


if __name__ == "__main__":
    main()
