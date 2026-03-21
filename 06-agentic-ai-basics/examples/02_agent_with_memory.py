"""
Module 06 - Example 2: Agent with Memory and Reflection
========================================================
An agent that maintains memory across interactions and reflects on its actions.

Pain Point: Agents forget everything between conversations.
Solution:   Explicit memory management + self-reflection.
"""

import json
import os
from datetime import datetime

from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


class AgentMemory:
    """Simple memory system with short-term and long-term storage."""

    def __init__(self):
        self.short_term: list[dict] = []   # Current conversation
        self.long_term: list[dict] = []    # Persists across conversations
        self.reflections: list[str] = []   # Lessons learned

    def add_short_term(self, entry: dict):
        self.short_term.append({**entry, "timestamp": datetime.now().isoformat()})
        # Keep last 10 entries
        if len(self.short_term) > 10:
            self.short_term = self.short_term[-10:]

    def add_long_term(self, entry: dict):
        self.long_term.append({**entry, "timestamp": datetime.now().isoformat()})

    def add_reflection(self, reflection: str):
        self.reflections.append(reflection)

    def get_context(self) -> str:
        """Build memory context string for the LLM."""
        parts = []
        if self.long_term:
            parts.append("## Long-term Memory (facts learned):")
            for entry in self.long_term[-5:]:
                parts.append(f"  - {entry}")
        if self.reflections:
            parts.append("\n## Past Reflections (lessons learned):")
            for r in self.reflections[-3:]:
                parts.append(f"  - {r}")
        if self.short_term:
            parts.append("\n## Recent Actions:")
            for entry in self.short_term[-5:]:
                parts.append(f"  - {entry}")
        return "\n".join(parts) if parts else "No memories yet."


# ============================================
# TOOLS
# ============================================
def search_knowledge(query: str) -> str:
    """Search a knowledge base."""
    kb = {
        "python best practices": "Use type hints, write tests, follow PEP 8, use virtual environments.",
        "docker optimization": "Use multi-stage builds, minimize layers, use .dockerignore, pin versions.",
        "api design": "Use REST conventions, version APIs, validate inputs, return proper status codes.",
    }
    for key, value in kb.items():
        if any(word in query.lower() for word in key.split()):
            return value
    return "No relevant information found."


def save_note(content: str) -> str:
    """Save a note to persistent storage."""
    return f"Note saved: {content}"


TOOL_MAP = {
    "search_knowledge": search_knowledge,
    "save_note": save_note,
}

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "search_knowledge",
            "description": "Search the knowledge base for information",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "save_note",
            "description": "Save an important note for future reference",
            "parameters": {
                "type": "object",
                "properties": {"content": {"type": "string"}},
                "required": ["content"],
            },
        },
    },
]


class ReflectiveAgent:
    """An agent that maintains memory and reflects on its actions."""

    def __init__(self):
        self.memory = AgentMemory()

    def _get_system_prompt(self) -> str:
        memory_context = self.memory.get_context()
        return f"""You are an AI assistant with MEMORY and SELF-REFLECTION capabilities.

## Your Memory:
{memory_context}

## Your Process:
1. Check your memory for relevant past context
2. Use tools if needed to gather information
3. Provide your answer
4. After answering, REFLECT: What did I learn? What could I improve?

## Reflection Format:
After each response, add a section:
[REFLECTION]: One sentence about what you learned or would do differently.

## Rules:
- Reference your memory when relevant
- Save important new information as notes
- Be transparent about what you know vs. what you're looking up
"""

    def chat(self, user_message: str) -> str:
        """Process a message with memory and reflection."""
        print(f"\n{'='*60}")
        print(f"👤 User: {user_message}")
        print(f"{'='*60}")

        # Show memory state
        if self.memory.long_term or self.memory.reflections:
            print(f"🧠 Memory contains: {len(self.memory.long_term)} facts, "
                  f"{len(self.memory.reflections)} reflections")

        messages = [
            {"role": "system", "content": self._get_system_prompt()},
            {"role": "user", "content": user_message},
        ]

        # Agent loop
        for _ in range(5):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=TOOL_SCHEMAS,
            )
            message = response.choices[0].message

            if message.tool_calls:
                messages.append(message)
                for tool_call in message.tool_calls:
                    func_name = tool_call.function.name
                    args = json.loads(tool_call.function.arguments)
                    print(f"  🔧 {func_name}({args})")

                    result = TOOL_MAP[func_name](**args)
                    print(f"  📊 {result}")

                    # Store in short-term memory
                    self.memory.add_short_term({
                        "action": func_name, "args": args, "result": result
                    })

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result,
                    })
            else:
                answer = message.content
                print(f"\n🤖 Agent: {answer}")

                # Extract and store reflection
                if "[REFLECTION]:" in answer:
                    reflection = answer.split("[REFLECTION]:")[1].strip()
                    self.memory.add_reflection(reflection)
                    print(f"  🪞 Stored reflection: {reflection}")

                # Store interaction in long-term memory
                self.memory.add_long_term({
                    "user_asked": user_message[:100],
                    "topic": "conversation",
                })

                return answer

        return "Max iterations reached."


def main():
    print("=" * 60)
    print("AGENT WITH MEMORY & REFLECTION")
    print("=" * 60)

    agent = ReflectiveAgent()

    # Conversation 1: The agent learns something
    agent.chat("What are the best practices for Python development?")

    # Conversation 2: The agent should remember we discussed Python
    agent.chat("Based on what we discussed, help me set up a new Python project.")

    # Conversation 3: New topic — agent should still remember past
    agent.chat("Now I want to containerize my Python project with Docker.")

    # Conversation 4: Test memory recall
    agent.chat("Can you summarize everything we've discussed so far?")

    print(f"\n{'='*60}")
    print("MEMORY STATE AT END:")
    print(f"{'='*60}")
    print(f"Long-term memories: {len(agent.memory.long_term)}")
    for mem in agent.memory.long_term:
        print(f"  📝 {mem}")
    print(f"\nReflections: {len(agent.memory.reflections)}")
    for ref in agent.memory.reflections:
        print(f"  🪞 {ref}")

    print(f"\n{'='*60}")
    print("KEY INSIGHT: Memory + Reflection = Learning Agent")
    print(f"{'='*60}")
    print("""
    This agent demonstrates:
    
    1. 🧠 SHORT-TERM MEMORY: Remembers tool results within a conversation
    2. 📚 LONG-TERM MEMORY: Carries facts across conversations
    3. 🪞 REFLECTION: Learns from each interaction
    4. 🔄 CONTEXT BUILDING: Uses memory to enrich future prompts
    
    This is how modern AI assistants maintain continuity!
    
    → Next: Module 07 explores MULTIPLE agents collaborating
    → Module 08 shows how to manage all this context efficiently
    """)


if __name__ == "__main__":
    main()
