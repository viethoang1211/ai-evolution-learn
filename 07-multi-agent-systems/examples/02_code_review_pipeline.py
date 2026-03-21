"""
Module 07 - Example 2: Code Review Pipeline (Agent Handoff)
============================================================
Agents hand off work to each other in a pipeline.
Each agent adds its own perspective.

Pattern: Pipeline with feedback loop.
"""

import json
import os

from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def agent_call(role: str, system_prompt: str, context: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": context},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content


def code_review_pipeline(code: str, max_revisions: int = 2) -> dict:
    """
    Pipeline: Coder → Security Reviewer → Performance Reviewer → Final
    If issues found, code goes back for revision.
    """
    print("=" * 60)
    print("CODE REVIEW PIPELINE")
    print("=" * 60)

    current_code = code
    history = []

    for revision in range(max_revisions + 1):
        print(f"\n--- Revision {revision} ---")

        # Stage 1: Security Review
        print("🔒 Security Reviewer analyzing...")
        security_review = agent_call(
            "Security Reviewer",
            """You are a security-focused code reviewer. Analyze code for:
            - SQL injection, XSS, command injection
            - Hardcoded secrets or credentials
            - Insecure cryptographic practices
            - Missing input validation
            - OWASP Top 10 vulnerabilities
            
            Output format:
            ISSUES: [list of issues found, or "None"]
            SEVERITY: [CRITICAL/HIGH/MEDIUM/LOW/NONE]
            VERDICT: [PASS/FAIL]""",
            f"Review this code:\n```python\n{current_code}\n```",
        )
        print(f"  {security_review[:200]}...")

        # Stage 2: Performance Review
        print("⚡ Performance Reviewer analyzing...")
        perf_review = agent_call(
            "Performance Reviewer",
            """You are a performance-focused code reviewer. Analyze code for:
            - Algorithmic complexity issues (O(n²) where O(n) is possible)
            - Memory leaks or excessive memory usage
            - Missing caching opportunities
            - Database N+1 query problems
            - Unnecessary string concatenation in loops
            
            Output format:
            ISSUES: [list of issues, or "None"]
            IMPACT: [HIGH/MEDIUM/LOW/NONE]
            VERDICT: [PASS/FAIL]""",
            f"Review this code:\n```python\n{current_code}\n```",
        )
        print(f"  {perf_review[:200]}...")

        # Check if reviews passed
        all_passed = "PASS" in security_review and "PASS" in perf_review
        history.append({
            "revision": revision,
            "security": security_review,
            "performance": perf_review,
            "passed": all_passed,
        })

        if all_passed or revision == max_revisions:
            break

        # Stage 3: Fix Agent — applies review feedback
        print("🔧 Fix Agent applying improvements...")
        current_code = agent_call(
            "Fix Agent",
            """You are a code improvement agent. Given code and review feedback,
            output the FIXED code that addresses all issues mentioned.
            Output ONLY the fixed Python code, no explanations.""",
            f"""Original code:
```python
{current_code}
```

Security Review:
{security_review}

Performance Review:
{perf_review}

Fix all issues and output the improved code.""",
        )
        # Clean up code markers
        if "```python" in current_code:
            current_code = current_code.split("```python")[1].split("```")[0].strip()
        print(f"  Updated code ({len(current_code)} chars)")

    # Final result
    print(f"\n{'='*60}")
    print("PIPELINE RESULT")
    print(f"{'='*60}")
    print(f"Total revisions: {len(history)}")
    print(f"Final verdict: {'PASSED ✅' if history[-1]['passed'] else 'NEEDS WORK ⚠️'}")
    print(f"\nFinal code:\n{current_code[:500]}...")

    return {
        "final_code": current_code,
        "history": history,
        "passed": history[-1]["passed"],
    }


def main():
    # Code with intentional issues for the pipeline to catch
    problematic_code = '''
import hashlib
import sqlite3

DB_PASSWORD = "admin123"  # Database password

def get_user(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # Build query with string concatenation
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result

def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

def process_users(user_list):
    result = ""
    for user in user_list:
        result = result + str(user) + "\\n"
    return result
'''

    result = code_review_pipeline(problematic_code)

    print(f"\n{'='*60}")
    print("KEY INSIGHT: Pipeline Pattern")
    print(f"{'='*60}")
    print("""
    The pipeline processed the code through multiple specialized reviewers:
    
    🔒 Security Agent caught:
       - SQL injection vulnerability
       - Hardcoded credentials
       - Weak hashing (MD5)
    
    ⚡ Performance Agent caught:
       - String concatenation in loop
       - Missing connection pooling
    
    🔧 Fix Agent then addressed all issues automatically!
    
    This is exactly how AI code review tools work in production.
    Each agent is an EXPERT in its domain.
    """)


if __name__ == "__main__":
    main()
