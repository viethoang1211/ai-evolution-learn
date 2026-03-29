"""
Module 10 - Complete Mini Agentic Coding Assistant
===================================================
This is the CAPSTONE example that combines ALL concepts from Modules 01–09
into a working mini agentic coding assistant.

Components used:
- Module 01: LLM as the reasoning core
- Module 02: Structured system prompt with persona
- Module 03: RAG-like context retrieval (code search)
- Module 04: Function calling / tools
- Module 05: ReAct loop (reason → act → observe)
- Module 06: Planning, memory, and reflection
- Module 07: Specialized sub-agents (code, test, review)
- Module 08: Dynamic context assembly
- Module 09: MCP-style tool registry

Requirements:
    pip install openai
"""

import json
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from utils.llm_client import get_client, get_model

client = get_client()


# ============================================
# MODULE 09: MCP-Style Tool Registry
# ============================================
class ToolRegistry:
    """Centralized tool registry (MCP pattern)."""

    def __init__(self):
        self._tools: dict[str, dict] = {}

    def register(self, name: str, description: str, schema: dict, handler: callable):
        self._tools[name] = {
            "name": name,
            "description": description,
            "schema": schema,
            "handler": handler,
        }

    def get_openai_tools(self) -> list[dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": t["name"],
                    "description": t["description"],
                    "parameters": t["schema"],
                },
            }
            for t in self._tools.values()
        ]

    def execute(self, name: str, arguments: dict) -> str:
        if name not in self._tools:
            return json.dumps({"error": f"Unknown tool: {name}"})
        try:
            result = self._tools[name]["handler"](**arguments)
            return json.dumps(result) if isinstance(result, dict) else str(result)
        except Exception as e:
            return json.dumps({"error": str(e)})


# ============================================
# SIMULATED CODEBASE (like a file system)
# ============================================
WORKSPACE = {
    "src/app.py": '''from fastapi import FastAPI
from src.routes import router

app = FastAPI(title="My API", version="0.1.0")
app.include_router(router, prefix="/api/v1")

@app.get("/health")
def health():
    return {"status": "ok"}
''',
    "src/routes.py": '''from fastapi import APIRouter, HTTPException

router = APIRouter()

# TODO: Add user routes
@router.get("/users")
def list_users():
    return {"users": []}
''',
    "src/models.py": '''from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
''',
    "tests/test_app.py": '''import pytest

def test_health():
    # TODO: implement
    assert True
''',
    "requirements.txt": "fastapi==0.109.0\nuvicorn==0.27.0\npydantic==2.5.0\n",
}


# ============================================
# MODULE 06: Agent Memory
# ============================================
class Memory:
    def __init__(self):
        self.actions: list[dict] = []
        self.plan: list[str] = []
        self.reflections: list[str] = []

    def log_action(self, tool: str, args: dict, result: str):
        self.actions.append({
            "tool": tool,
            "args": args,
            "result": result[:200],
            "time": datetime.now().isoformat(),
        })

    def get_summary(self) -> str:
        parts = []
        if self.plan:
            parts.append("Current Plan: " + " → ".join(self.plan))
        if self.actions:
            recent = self.actions[-5:]
            parts.append("Recent Actions: " + "; ".join(
                f"{a['tool']}({a['args']})" for a in recent
            ))
        if self.reflections:
            parts.append("Lessons: " + "; ".join(self.reflections[-3:]))
        return "\n".join(parts) if parts else "No history yet."


# ============================================
# REGISTER TOOLS (Module 04 + 09)
# ============================================
registry = ToolRegistry()

# Tool: Read file
def read_file(path: str) -> dict:
    if path in WORKSPACE:
        return {"path": path, "content": WORKSPACE[path]}
    return {"error": f"File not found: {path}"}

registry.register("read_file", "Read a file from the workspace", {
    "type": "object",
    "properties": {"path": {"type": "string", "description": "File path"}},
    "required": ["path"],
}, read_file)

# Tool: Write file
def write_file(path: str, content: str) -> dict:
    WORKSPACE[path] = content
    return {"success": True, "path": path, "size": len(content)}

registry.register("write_file", "Write content to a file (create or overwrite)", {
    "type": "object",
    "properties": {
        "path": {"type": "string"},
        "content": {"type": "string", "description": "File content to write"},
    },
    "required": ["path", "content"],
}, write_file)

# Tool: List files
def list_files(directory: str = "") -> dict:
    files = [f for f in WORKSPACE if f.startswith(directory)]
    return {"files": files}

registry.register("list_files", "List files in the workspace", {
    "type": "object",
    "properties": {
        "directory": {"type": "string", "description": "Directory prefix filter"},
    },
}, list_files)

# Tool: Search code (Module 03 - RAG-like)
def search_code(query: str) -> dict:
    results = []
    for path, content in WORKSPACE.items():
        if query.lower() in content.lower():
            # Find matching lines
            for i, line in enumerate(content.split("\n"), 1):
                if query.lower() in line.lower():
                    results.append({"file": path, "line": i, "text": line.strip()})
    return {"query": query, "matches": results[:10]}

registry.register("search_code", "Search for text across all files in the workspace", {
    "type": "object",
    "properties": {
        "query": {"type": "string", "description": "Text to search for"},
    },
    "required": ["query"],
}, search_code)

# Tool: Run tests
def run_tests(path: str = "tests/") -> dict:
    test_files = [f for f in WORKSPACE if f.startswith(path) and "test" in f]
    results = []
    for tf in test_files:
        content = WORKSPACE[tf]
        num_tests = content.count("def test_")
        num_asserts = content.count("assert")
        results.append({
            "file": tf,
            "tests_found": num_tests,
            "assertions": num_asserts,
            "status": "passed" if num_asserts > 0 else "no assertions",
        })
    return {"test_results": results}

registry.register("run_tests", "Run tests in the workspace", {
    "type": "object",
    "properties": {
        "path": {"type": "string", "description": "Test directory or file"},
    },
}, run_tests)


# ============================================
# MODULE 08: Dynamic Context Assembly
# ============================================
def build_context(task: str, memory: Memory) -> str:
    """Assemble context dynamically based on the task."""
    context_parts = [
        # Module 02: System prompt
        """## Role
You are an expert AI coding assistant working on a FastAPI Python project.
You follow clean code principles, write tests, and think step by step.

## Workflow
1. PLAN: Analyze the task and outline your approach
2. EXPLORE: Read relevant existing code
3. IMPLEMENT: Make changes using the available tools
4. VERIFY: Run tests to validate your changes
5. REPORT: Summarize what you did

## Rules
- Always read existing code before modifying
- Write tests for new functionality
- Explain your reasoning at each step
""",
        # Module 06: Memory context
        f"## Context from Memory\n{memory.get_summary()}",

        # Module 08: Available files overview
        f"## Workspace Files\n{json.dumps(list(WORKSPACE.keys()), indent=2)}",
    ]

    return "\n\n".join(context_parts)


# ============================================
# MODULE 05 + 06: The Agentic Loop
# ============================================
def run_agent(task: str, max_steps: int = 12) -> str:
    """
    The complete agentic loop combining:
    - ReAct (Module 05): Thought → Action → Observation
    - Planning (Module 06): Plan before acting
    - Memory (Module 06): Track actions and learn
    - Context Engineering (Module 08): Dynamic context assembly
    - Tool Registry (Module 09): MCP-style tool access
    """
    memory = Memory()

    print(f"\n{'='*70}")
    print(f"🎯 TASK: {task}")
    print(f"{'='*70}")

    # Build dynamic context
    system_context = build_context(task, memory)
    tools = registry.get_openai_tools()

    messages = [
        {"role": "system", "content": system_context},
        {"role": "user", "content": task},
    ]

    for step in range(max_steps):
        print(f"\n--- Step {step + 1} ---")

        response = client.chat.completions.create(
            model=get_model(),
            messages=messages,
            tools=tools,
        )
        message = response.choices[0].message

        # Display reasoning (Module 05: Thought)
        if message.content:
            print(f"💭 {message.content[:300]}{'...' if len(message.content or '') > 300 else ''}")

        # Execute tools (Module 05: Action)
        if message.tool_calls:
            messages.append(message)
            for tool_call in message.tool_calls:
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

                display_args = {k: (v[:60] + "...") if isinstance(v, str) and len(v) > 60 else v
                               for k, v in args.items()}
                print(f"🔧 {name}({display_args})")

                # Execute via registry (Module 09: MCP routing)
                result = registry.execute(name, args)

                # Module 05: Observation
                print(f"👁️ {result[:150]}{'...' if len(result) > 150 else ''}")

                # Module 06: Memory
                memory.log_action(name, display_args, result)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                })
        else:
            # Final answer — agent is done
            print(f"\n✅ TASK COMPLETE")
            print(f"{'='*70}")
            print(f"📝 Summary:\n{message.content}")
            print(f"\n📊 Agent Stats:")
            print(f"   Steps taken: {step + 1}")
            print(f"   Tools called: {len(memory.actions)}")
            print(f"   Tool breakdown: {json.dumps({a['tool']: 1 for a in memory.actions})}")
            return message.content

    return "Max steps reached."


# ============================================
# MAIN: Run the complete agent
# ============================================
def main():
    print("=" * 70)
    print("🤖 MINI AGENTIC CODING ASSISTANT")
    print("   Combining ALL concepts from Modules 01-09")
    print("=" * 70)

    # Task 1: Feature implementation
    run_agent(
        """Add a POST /api/v1/users endpoint that:
        1. Accepts a JSON body with name and email
        2. Validates the email format
        3. Returns the created user with an auto-generated ID
        4. Update tests to cover the new endpoint"""
    )

    # Show final state of workspace
    print(f"\n{'='*70}")
    print("📁 FINAL WORKSPACE STATE")
    print(f"{'='*70}")
    for path, content in sorted(WORKSPACE.items()):
        print(f"\n📄 {path}:")
        print("-" * 40)
        print(content[:400])
        if len(content) > 400:
            print("...")

    print(f"\n{'='*70}")
    print("🎓 COURSE COMPLETE: From LLM to Agentic AI")
    print(f"{'='*70}")
    print("""
    You've seen the COMPLETE evolution:
    
    Module 01: LLM Foundations     → The reasoning engine
    Module 02: Prompt Engineering  → Controlling the engine
    Module 03: RAG                 → Grounding in real data
    Module 04: Function Calling    → Connecting to the world
    Module 05: ReAct               → Reasoning + Acting loop
    Module 06: Agentic AI          → Planning + Memory + Reflection
    Module 07: Multi-Agent         → Teams of specialized agents
    Module 08: Context Engineering → Managing information flow
    Module 09: MCP & Skills        → Standardized tool ecosystem
    Module 10: Everything Together → Modern AI assistants
    
    Each innovation was driven by a REAL PAIN POINT.
    Each solution built on the previous ones.
    
    The future is being built on these foundations. 🚀
    """)


if __name__ == "__main__":
    main()
