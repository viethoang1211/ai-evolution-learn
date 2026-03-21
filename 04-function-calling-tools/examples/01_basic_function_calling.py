"""
Module 04 - Example 1: Basic Function Calling
==============================================
Implement the complete function calling flow with OpenAI.

Pain Point Solved: LLMs can now interact with external systems.

Requirements:
    pip install openai
"""

import json
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# ============================================
# STEP 1: Define the tools (functions)
# ============================================

# These are SIMULATED tool implementations
# In production, these would call real APIs
def get_weather(city: str, unit: str = "celsius") -> dict:
    """Simulated weather API."""
    weather_data = {
        "Tokyo": {"temp": 22, "condition": "Sunny", "humidity": 45},
        "London": {"temp": 15, "condition": "Cloudy", "humidity": 78},
        "New York": {"temp": 28, "condition": "Partly Cloudy", "humidity": 55},
    }
    data = weather_data.get(city, {"temp": 20, "condition": "Unknown", "humidity": 50})
    if unit == "fahrenheit":
        data["temp"] = round(data["temp"] * 9 / 5 + 32)
    data["unit"] = unit
    data["city"] = city
    return data


def calculate(expression: str) -> dict:
    """Safely evaluate a mathematical expression."""
    # Only allow safe mathematical operations
    allowed_chars = set("0123456789+-*/().% ")
    if not all(c in allowed_chars for c in expression):
        return {"error": "Invalid expression — only math operations allowed"}
    try:
        result = eval(expression)  # Safe because we validated input
        return {"expression": expression, "result": result}
    except Exception as e:
        return {"error": str(e)}


def search_products(query: str, max_price: float | None = None) -> dict:
    """Simulated product search."""
    products = [
        {"name": "MacBook Pro 16\"", "price": 2499, "category": "laptop"},
        {"name": "ThinkPad X1 Carbon", "price": 1649, "category": "laptop"},
        {"name": "Dell XPS 15", "price": 1899, "category": "laptop"},
        {"name": "Magic Mouse", "price": 99, "category": "accessory"},
        {"name": "Mechanical Keyboard", "price": 149, "category": "accessory"},
    ]
    results = [p for p in products if query.lower() in p["name"].lower()
               or query.lower() in p["category"].lower()]
    if max_price:
        results = [p for p in results if p["price"] <= max_price]
    return {"query": query, "results": results, "count": len(results)}


# Map function names to actual implementations
TOOL_IMPLEMENTATIONS = {
    "get_weather": get_weather,
    "calculate": calculate,
    "search_products": search_products,
}

# ============================================
# STEP 2: Define tool schemas for the LLM
# ============================================
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather information for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city name, e.g., 'Tokyo', 'London'",
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "Temperature unit (default: celsius)",
                    },
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a mathematical expression",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Math expression to evaluate, e.g., '(15 * 3) + 42'",
                    }
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_products",
            "description": "Search for products in the catalog",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query for products",
                    },
                    "max_price": {
                        "type": "number",
                        "description": "Maximum price filter (optional)",
                    },
                },
                "required": ["query"],
            },
        },
    },
]


# ============================================
# STEP 3: The function calling loop
# ============================================
def chat_with_tools(user_message: str) -> str:
    """Complete function calling flow."""
    print(f"\n📝 User: {user_message}")

    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant. Use the provided tools when needed.",
        },
        {"role": "user", "content": user_message},
    ]

    # First API call — LLM decides whether to use tools
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=TOOLS,
    )
    message = response.choices[0].message

    # Check if the LLM wants to call tools
    if message.tool_calls:
        # Add the assistant's message (with tool calls) to history
        messages.append(message)

        # Execute each tool call
        for tool_call in message.tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            print(f"🔧 Tool call: {function_name}({arguments})")

            # Execute the function
            func = TOOL_IMPLEMENTATIONS[function_name]
            result = func(**arguments)

            print(f"📊 Result: {result}")

            # Add tool result to messages
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result),
            })

        # Second API call — LLM processes tool results
        final_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        return final_response.choices[0].message.content
    else:
        # No tool needed — direct response
        return message.content


# ============================================
# STEP 4: Demo
# ============================================
def main():
    print("=" * 60)
    print("FUNCTION CALLING DEMO")
    print("=" * 60)

    queries = [
        "What's the weather like in Tokyo?",
        "Calculate: if I have 3 items at $49.99 each with 8.5% tax, what's the total?",
        "Show me laptops under $2000",
        "What's the weather in London and also find me some accessories under $150?",
        "What's 2 + 2?",  # LLM might answer directly without tools
    ]

    for query in queries:
        print("\n" + "=" * 60)
        answer = chat_with_tools(query)
        print(f"\n🤖 Answer: {answer}")

    print("\n" + "=" * 60)
    print("KEY INSIGHT: The LLM DECIDED when to use tools vs. answer directly!")
    print("This is the foundation of agentic behavior.")
    print("=" * 60)


if __name__ == "__main__":
    main()
