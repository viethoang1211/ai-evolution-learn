"""
Module 05 - Example 1: ReAct Agent from Scratch
================================================
Build a ReAct (Reasoning + Acting) agent using pure Python + OpenAI.
No frameworks — understand the core loop.

This is THE pattern behind every modern AI agent.

Requirements:
    pip install openai
"""

import json
import os

from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


# ============================================
# TOOLS: Simulated external services
# ============================================
def search_web(query: str) -> str:
    """Simulated web search."""
    fake_results = {
        "python 3.12 new features": (
            "Python 3.12 introduced: improved error messages, "
            "f-string improvements, per-interpreter GIL (PEP 684), "
            "and the new type statement (PEP 695)."
        ),
        "population of tokyo": "Tokyo metro area population: approximately 37.4 million (2024).",
        "distance earth to mars": (
            "The distance from Earth to Mars varies: minimum ~54.6 million km, "
            "maximum ~401 million km, average ~225 million km."
        ),
    }
    for key, value in fake_results.items():
        if any(word in query.lower() for word in key.split()):
            return value
    return f"No results found for: {query}"


def calculator(expression: str) -> str:
    """Safe mathematical calculator."""
    allowed_chars = set("0123456789+-*/(). eE")
    if not all(c in allowed_chars for c in expression):
        return f"Error: Invalid characters in expression"
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {e}"


def get_current_date() -> str:
    """Get today's date."""
    from datetime import date
    return date.today().isoformat()


TOOLS = {
    "search_web": {
        "fn": search_web,
        "schema": {
            "type": "function",
            "function": {
                "name": "search_web",
                "description": "Search the web for information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"}
                    },
                    "required": ["query"],
                },
            },
        },
    },
    "calculator": {
        "fn": calculator,
        "schema": {
            "type": "function",
            "function": {
                "name": "calculator",
                "description": "Calculate a mathematical expression",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description": "Math expression like '(37.4 * 1000000) / 2'",
                        }
                    },
                    "required": ["expression"],
                },
            },
        },
    },
    "get_current_date": {
        "fn": get_current_date,
        "schema": {
            "type": "function",
            "function": {
                "name": "get_current_date",
                "description": "Get today's date",
                "parameters": {"type": "object", "properties": {}},
            },
        },
    },
}

# ============================================
# THE ReAct AGENT
# ============================================
REACT_SYSTEM_PROMPT = """You are a ReAct agent. You solve problems by interleaving 
THINKING and ACTING in a loop.

For each step, you should:
1. THINK about what you know and what you need to find out
2. Decide on an ACTION (use a tool) or give a FINAL ANSWER

You have access to these tools:
- search_web(query): Search the web for information
- calculator(expression): Calculate math expressions  
- get_current_date(): Get today's date

Important rules:
- Always think before acting
- Use observations from tools to inform your next thought
- If a search doesn't give you what you need, try a different query
- When you have enough information, provide a clear final answer
"""


def react_agent(question: str, max_steps: int = 6) -> str:
    """
    The ReAct loop:
    1. Send question + conversation history to LLM
    2. LLM either calls a tool (ACTION) or gives final answer
    3. If tool called: execute it, add OBSERVATION, go to step 1
    4. If final answer: return it
    """
    print(f"\n{'='*60}")
    print(f"❓ Question: {question}")
    print(f"{'='*60}")

    messages = [
        {"role": "system", "content": REACT_SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]

    tool_schemas = [t["schema"] for t in TOOLS.values()]

    for step in range(max_steps):
        print(f"\n--- Step {step + 1} ---")

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tool_schemas,
        )
        message = response.choices[0].message

        # If the LLM wants to reason (text content with tool calls, or just text)
        if message.content:
            print(f"💭 Thought: {message.content}")

        # Check if LLM wants to use a tool
        if message.tool_calls:
            messages.append(message)

            for tool_call in message.tool_calls:
                func_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

                print(f"🔧 Action: {func_name}({args})")

                # Execute the tool
                tool_fn = TOOLS[func_name]["fn"]
                result = tool_fn(**args)

                print(f"👁️ Observation: {result}")

                # Feed observation back to the LLM
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                })
        else:
            # No tool calls — this is the final answer
            print(f"\n✅ Final Answer: {message.content}")
            return message.content

    return "Reached maximum steps without a final answer."


# ============================================
# DEMO
# ============================================
def main():
    print("=" * 60)
    print("ReAct AGENT DEMO — Reasoning + Acting")
    print("=" * 60)

    # Query 1: Simple — needs one search
    react_agent("What are the new features in Python 3.12?")

    # Query 2: Multi-step — needs search + calculation
    react_agent(
        "What is the population of Tokyo? If every person ate 2 meals "
        "per day, how many total meals would that be per year?"
    )

    # Query 3: Complex — needs multiple searches + reasoning
    react_agent(
        "What is the average distance from Earth to Mars in km? "
        "How long would it take to travel there at 100,000 km/h? "
        "Convert that to days."
    )

    print("\n" + "=" * 60)
    print("KEY INSIGHT: Notice the Thought → Action → Observation loop!")
    print("The agent REASONS about each result before deciding what to do next.")
    print("This is fundamentally different from blind function calling.")
    print("=" * 60)


if __name__ == "__main__":
    main()
