"""
Module 04 - Example 2: Multi-Tool Assistant
============================================
A more realistic assistant that chains multiple tools together.
Shows how the LLM orchestrates tools to complete complex tasks.

Pain Point: Real tasks often require multiple tools in sequence.
Preview: This manual orchestration will evolve into ReAct (Module 05).
"""

import json
import os
from datetime import datetime

from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


# ============================================
# Simulated tools for a project management assistant
# ============================================
# In-memory "databases"
TASKS_DB = {
    "PROJ-101": {"title": "Fix login bug", "status": "in_progress", "assignee": "alice", "priority": "high"},
    "PROJ-102": {"title": "Add dark mode", "status": "todo", "assignee": "bob", "priority": "medium"},
    "PROJ-103": {"title": "Update API docs", "status": "done", "assignee": "alice", "priority": "low"},
    "PROJ-104": {"title": "Database migration", "status": "in_progress", "assignee": "charlie", "priority": "high"},
}

TEAM_DB = {
    "alice": {"name": "Alice Chen", "role": "Senior Engineer", "active_tasks": 2},
    "bob": {"name": "Bob Smith", "role": "Frontend Dev", "active_tasks": 1},
    "charlie": {"name": "Charlie Wang", "role": "Backend Dev", "active_tasks": 1},
}


def get_task(task_id: str) -> dict:
    task = TASKS_DB.get(task_id.upper())
    if task:
        return {"task_id": task_id.upper(), **task}
    return {"error": f"Task {task_id} not found"}


def list_tasks(status: str | None = None, assignee: str | None = None) -> dict:
    results = []
    for tid, task in TASKS_DB.items():
        if status and task["status"] != status:
            continue
        if assignee and task["assignee"] != assignee:
            continue
        results.append({"task_id": tid, **task})
    return {"tasks": results, "count": len(results)}


def update_task_status(task_id: str, new_status: str) -> dict:
    task_id = task_id.upper()
    if task_id not in TASKS_DB:
        return {"error": f"Task {task_id} not found"}
    old_status = TASKS_DB[task_id]["status"]
    TASKS_DB[task_id]["status"] = new_status
    return {"task_id": task_id, "old_status": old_status, "new_status": new_status, "updated": True}


def get_team_member(username: str) -> dict:
    member = TEAM_DB.get(username.lower())
    if member:
        return {"username": username.lower(), **member}
    return {"error": f"Team member {username} not found"}


def get_current_time() -> dict:
    return {"current_time": datetime.now().isoformat(), "timezone": "UTC"}


TOOL_MAP = {
    "get_task": get_task,
    "list_tasks": list_tasks,
    "update_task_status": update_task_status,
    "get_team_member": get_team_member,
    "get_current_time": get_current_time,
}

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_task",
            "description": "Get details of a specific task by ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "Task ID like PROJ-101"}
                },
                "required": ["task_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "List tasks, optionally filtered by status and/or assignee",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["todo", "in_progress", "done"],
                        "description": "Filter by task status",
                    },
                    "assignee": {"type": "string", "description": "Filter by assignee username"},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_task_status",
            "description": "Update the status of a task",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "Task ID to update"},
                    "new_status": {
                        "type": "string",
                        "enum": ["todo", "in_progress", "done"],
                        "description": "New status",
                    },
                },
                "required": ["task_id", "new_status"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_team_member",
            "description": "Get info about a team member",
            "parameters": {
                "type": "object",
                "properties": {
                    "username": {"type": "string", "description": "Team member username"}
                },
                "required": ["username"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get the current date and time",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]


def run_assistant(user_message: str):
    """Run the multi-tool assistant with a tool-calling loop."""
    print(f"\n{'='*60}")
    print(f"📝 User: {user_message}")
    print("-" * 60)

    messages = [
        {
            "role": "system",
            "content": """You are a project management assistant. Use the available 
tools to help manage tasks and team information. Be concise and helpful.
When you need to perform multiple lookups, make all tool calls at once if possible.""",
        },
        {"role": "user", "content": user_message},
    ]

    # Tool-calling loop — keep going until the LLM gives a final response
    max_iterations = 5
    for i in range(max_iterations):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=TOOLS,
        )
        message = response.choices[0].message

        if not message.tool_calls:
            # No more tool calls — we have our final answer
            print(f"\n🤖 Assistant: {message.content}")
            return message.content

        # Process tool calls
        messages.append(message)
        for tool_call in message.tool_calls:
            func_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            print(f"  🔧 [{i+1}] {func_name}({args})")

            result = TOOL_MAP[func_name](**args)
            print(f"  📊 Result: {json.dumps(result, indent=2)}")

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result),
            })

    return "Max iterations reached"


def main():
    print("=" * 60)
    print("MULTI-TOOL PROJECT MANAGEMENT ASSISTANT")
    print("=" * 60)

    # Simple query — single tool
    run_assistant("What's the status of PROJ-101?")

    # Multi-step query — needs to check multiple things
    run_assistant("What are all of Alice's current tasks?")

    # Action + query — update then verify
    run_assistant("Mark the API docs task as done and show me all completed tasks.")

    # Complex query — needs multiple tools
    run_assistant(
        "Give me a status report: how many tasks are in progress, "
        "who's working on high priority items, and what time is it?"
    )

    print("\n" + "=" * 60)
    print("EVOLUTION PREVIEW:")
    print("=" * 60)
    print("""
    What we just built is CLOSE TO but NOT YET an agent.
    
    Current (Function Calling):
    ✅ LLM decides WHICH tools to call
    ✅ LLM processes tool results
    ✅ Can chain multiple tool calls
    
    What's missing (solved in Modules 05-06):
    ❌ No explicit reasoning/planning step
    ❌ No error recovery strategy
    ❌ No ability to re-plan based on results
    
    → ReAct (Module 05) adds Thought-Action-Observation loops
    → Agentic AI (Module 06) adds planning and autonomy
    """)


if __name__ == "__main__":
    main()
