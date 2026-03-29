"""
Module 06 - Example 1: Planning Agent
======================================
A full agentic AI that PLANS before acting, then executes step by step.

This is the key upgrade from ReAct: explicit planning.

Requirements:
    pip install openai
"""

import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from utils.llm_client import get_client, get_model

client = get_client()


# ============================================
# TOOLS for a coding assistant agent
# ============================================
FILE_SYSTEM = {}  # Simulated file system


def read_file(path: str) -> str:
    if path in FILE_SYSTEM:
        return FILE_SYSTEM[path]
    return f"Error: File '{path}' not found"


def write_file(path: str, content: str) -> str:
    FILE_SYSTEM[path] = content
    return f"Successfully wrote {len(content)} chars to {path}"


def list_files(directory: str = ".") -> str:
    files = [f for f in FILE_SYSTEM if f.startswith(directory)]
    return json.dumps(files) if files else "No files found"


def run_tests(test_file: str) -> str:
    """Simulated test runner."""
    if test_file not in FILE_SYSTEM:
        return f"Error: Test file '{test_file}' not found"
    content = FILE_SYSTEM[test_file]
    # Simulate: tests pass if they contain 'assert' statements
    assert_count = content.count("assert")
    if assert_count > 0:
        return f"Ran {assert_count} tests. All passed! ✅"
    return "No tests found in file."


TOOL_MAP = {
    "read_file": read_file,
    "write_file": write_file,
    "list_files": list_files,
    "run_tests": run_tests,
}

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a file's contents",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a file (creates or overwrites)",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "content": {"type": "string", "description": "File content"},
                },
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List files in a directory",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {"type": "string", "description": "Directory path (default: '.')"},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_tests",
            "description": "Run tests in a test file and return results",
            "parameters": {
                "type": "object",
                "properties": {
                    "test_file": {"type": "string", "description": "Path to test file"},
                },
                "required": ["test_file"],
            },
        },
    },
]


# ============================================
# THE PLANNING AGENT
# ============================================
AGENT_SYSTEM_PROMPT = """You are an AI coding agent that follows a strict workflow:

## WORKFLOW
1. **PLAN**: Before doing anything, create a numbered plan of steps.
2. **EXECUTE**: Carry out each step using the available tools.
3. **VERIFY**: After implementation, always run tests to verify.
4. **REPORT**: Summarize what you did and the final state.

## RULES
- Always plan before coding
- Write tests for every function you create
- If tests fail, debug and fix
- Keep code clean and well-structured

## AVAILABLE TOOLS
- read_file(path): Read a file
- write_file(path, content): Write a file
- list_files(directory): List files
- run_tests(test_file): Run tests
"""


def planning_agent(goal: str, max_steps: int = 15) -> str:
    """Agent that plans, executes, and verifies."""
    print(f"\n{'='*60}")
    print(f"🎯 Goal: {goal}")
    print(f"{'='*60}")

    messages = [
        {"role": "system", "content": AGENT_SYSTEM_PROMPT},
        {"role": "user", "content": goal},
    ]

    for step in range(max_steps):
        response = client.chat.completions.create(
            model=get_model(),
            messages=messages,
            tools=TOOL_SCHEMAS,
        )
        message = response.choices[0].message

        if message.content:
            print(f"\n💭 Agent: {message.content}")

        if message.tool_calls:
            messages.append(message)
            for tool_call in message.tool_calls:
                func_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

                # Truncate content for display
                display_args = {k: (v[:80] + "...") if isinstance(v, str) and len(v) > 80 else v
                               for k, v in args.items()}
                print(f"🔧 Action: {func_name}({display_args})")

                result = TOOL_MAP[func_name](**args)
                print(f"📊 Result: {result}")

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                })
        else:
            # Final response
            print(f"\n✅ Agent completed!")
            return message.content

    return "Max steps reached."


def main():
    print("=" * 60)
    print("PLANNING AGENT DEMO")
    print("=" * 60)

    # Give the agent a complex, multi-step coding task
    result = planning_agent(
        """Create a Python module for a simple calculator with these requirements:
        
        1. Create a file 'calculator.py' with functions: add, subtract, multiply, divide
        2. The divide function should handle division by zero gracefully
        3. Create a file 'test_calculator.py' with tests for all functions
        4. Run the tests to verify everything works
        
        Make sure the code is clean and well-documented."""
    )

    # Show the files that were created
    print(f"\n{'='*60}")
    print("FILES CREATED BY THE AGENT:")
    print(f"{'='*60}")
    for path, content in FILE_SYSTEM.items():
        print(f"\n📄 {path}:")
        print("-" * 40)
        print(content)

    print(f"\n{'='*60}")
    print("KEY DIFFERENCE FROM ReAct:")
    print(f"{'='*60}")
    print("""
    ReAct Agent:     Think → Act → Observe → Think → Act → ...
    Planning Agent:  PLAN → [Execute → Verify] per step → REPORT
    
    The planning phase makes the agent more:
    ✅ Organized — knows the full scope before starting
    ✅ Efficient — doesn't wander or repeat steps
    ✅ Verifiable — has a checklist to check off
    ✅ Transparent — user can see the plan upfront
    """)


if __name__ == "__main__":
    main()
