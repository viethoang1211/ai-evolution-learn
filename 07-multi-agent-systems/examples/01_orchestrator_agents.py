"""
Module 07 - Example 1: Orchestrator Multi-Agent System
======================================================
Build a team of specialized agents coordinated by an orchestrator.

Pain Point: Single agents struggle with complex multi-domain tasks.
Solution:   Specialized agents + orchestrator coordination.

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
# SPECIALIZED AGENTS
# ============================================
def call_agent(system_prompt: str, task: str, agent_name: str) -> str:
    """Call a specialized agent with its own system prompt."""
    print(f"\n  🤖 [{agent_name}] Working on: {task[:80]}...")
    response = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": task},
        ],
        temperature=0.3,
    )
    result = response.choices[0].message.content
    print(f"  ✅ [{agent_name}] Done ({len(result)} chars)")
    return result


# Agent personas
ARCHITECT_PROMPT = """You are a Senior Software Architect. Your job is to:
- Design system architecture from requirements
- Define API contracts and data models
- Choose appropriate technologies and patterns
- Output clear, structured technical specifications

Be concise. Output a structured spec, not prose."""

CODER_PROMPT = """You are an Expert Python Developer. Your job is to:
- Implement code from technical specifications
- Follow best practices: type hints, docstrings, error handling
- Write clean, production-ready code
- Only output Python code with brief comments

Output ONLY executable Python code."""

REVIEWER_PROMPT = """You are a Senior Code Reviewer. Your job is to:
- Review code for bugs, security issues, and best practices
- Check adherence to the technical specification
- Suggest specific improvements with code examples
- Rate overall quality: PASS, NEEDS_CHANGES, or FAIL

Be specific and constructive. Reference exact line issues."""

ORCHESTRATOR_PROMPT = """You are a Project Manager orchestrating a development team.
You receive a user's request and break it into tasks for your team:

Team members:
1. ARCHITECT - Designs the system, creates specs
2. CODER - Implements code from specs
3. REVIEWER - Reviews code quality

Your job:
- Analyze the user's request
- Create a clear task breakdown
- After receiving all outputs, synthesize a final deliverable

Output a JSON object with:
{
    "architect_task": "Task description for the architect",
    "coder_task": "Task description for the coder (will include architect's spec)",
    "summary": "Brief description of the project"
}"""


# ============================================
# THE ORCHESTRATOR
# ============================================
def orchestrate(user_request: str) -> dict:
    """
    Orchestrator pattern:
    1. Manager breaks task into sub-tasks
    2. Each specialist handles their part
    3. Results flow from architect → coder → reviewer
    """
    print("=" * 60)
    print(f"📋 User Request: {user_request}")
    print("=" * 60)

    # Step 1: Orchestrator creates task breakdown
    print("\n🎯 PHASE 1: Planning (Orchestrator)")
    plan_response = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": ORCHESTRATOR_PROMPT},
            {"role": "user", "content": user_request},
        ],
        response_format={"type": "json_object"},
        temperature=0.3,
    )
    plan = json.loads(plan_response.choices[0].message.content)
    print(f"  📝 Plan: {json.dumps(plan, indent=2)}")

    # Step 2: Architect designs the system
    print("\n🏗️ PHASE 2: Architecture")
    architecture = call_agent(
        ARCHITECT_PROMPT, plan["architect_task"], "Architect"
    )

    # Step 3: Coder implements based on architecture
    print("\n💻 PHASE 3: Implementation")
    coder_task = f"""Technical Specification:
{architecture}

Additional Requirements:
{plan['coder_task']}

Implement this specification in Python."""

    code = call_agent(CODER_PROMPT, coder_task, "Coder")

    # Step 4: Reviewer checks the code
    print("\n🔍 PHASE 4: Code Review")
    review_task = f"""## Original Specification:
{architecture}

## Implementation to Review:
```python
{code}
```

Review this implementation against the specification."""

    review = call_agent(REVIEWER_PROMPT, review_task, "Reviewer")

    # Final output
    result = {
        "architecture": architecture,
        "code": code,
        "review": review,
    }

    print("\n" + "=" * 60)
    print("📦 FINAL DELIVERABLE")
    print("=" * 60)
    print(f"\n📐 Architecture:\n{architecture[:500]}...")
    print(f"\n💻 Code:\n{code[:500]}...")
    print(f"\n🔍 Review:\n{review[:500]}...")

    return result


def main():
    # Test with a real-ish project request
    result = orchestrate(
        """Build a REST API endpoint for user registration that:
        - Accepts email and password
        - Validates email format
        - Hashes the password
        - Returns a JWT token
        - Handles duplicate email errors"""
    )

    print("\n" + "=" * 60)
    print("KEY INSIGHT: Multi-Agent Collaboration")
    print("=" * 60)
    print("""
    What happened:
    
    1. 🎯 ORCHESTRATOR broke the task into specialized sub-tasks
    2. 🏗️ ARCHITECT designed the system (API spec, data model)
    3. 💻 CODER implemented from the spec (not from vague request)
    4. 🔍 REVIEWER caught issues the coder might have missed
    
    This is better than a single agent because:
    ✅ Each agent has a FOCUSED system prompt
    ✅ Architect's output CONSTRAINS the coder (less hallucination)
    ✅ Reviewer provides quality control
    ✅ Each agent's context window is smaller and cleaner
    
    → This is how Devin, Copilot Workspace, and similar tools work!
    """)


if __name__ == "__main__":
    main()
