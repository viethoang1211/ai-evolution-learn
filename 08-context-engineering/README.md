# Module 08: Context Engineering — The New Paradigm

## 🎯 Learning Objectives
- Understand how "Prompt Engineering" evolved into "Context Engineering"
- Learn to design the full information environment around an LLM call
- Master context window management: what to include, what to trim, when to summarize
- See why this is the #1 skill for building production AI systems

---

## 🔴 Pain Point: Prompt Engineering Isn't Enough

As AI systems grew from chatbots to agents, a critical problem emerged:

```
2023 — Prompt Engineering:
  "Write a good prompt, get a good result."
  
  system_prompt = "You are a helpful assistant."       ← Simple!
  user_message = "Write a sort function."

2025 — Reality of Agentic AI:
  "Fill the context window with EXACTLY the right information."
  
  context = {
      system_prompt: "...",          ← Agent persona + rules
      instructions: "...",           ← Task-specific guidelines  
      user_preferences: "...",       ← Learned from memory
      retrieved_docs: "...",         ← RAG results
      tool_definitions: "...",       ← Available tools + schemas
      conversation_history: "...",   ← Summarized + recent
      recent_tool_results: "...",    ← Action observations
      code_context: "...",           ← Relevant source files
      error_logs: "...",             ← Recent failures
  }
  # All of this must fit in the context window!
```

> **Andrej Karpathy (2025):** "I think the term 'prompt engineering' is evolving into something much broader — **context engineering**. It's not just about the prompt anymore. It's about carefully curating all the information that goes into that context window."

---

## 📖 Prompt Engineering vs. Context Engineering

| Aspect | Prompt Engineering | Context Engineering |
|--------|-------------------|-------------------|
| **Scope** | The user message | The entire context window |
| **Components** | Prompt text | System prompt + memory + RAG + tools + history + state |
| **Challenge** | "How do I phrase this?" | "What information does the model need to succeed?" |
| **Skill** | Writing good prompts | Designing information systems |
| **Analogy** | Writing a good question | Preparing a complete briefing package |
| **Era** | 2023 (ChatGPT) | 2025 (Agentic AI) |

---

## 📊 The Context Window: Your Most Precious Resource

```
┌─────────────────────────────────────────────────────────────┐
│            CONTEXT WINDOW (e.g., 128K tokens)                │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ SYSTEM PROMPT                              ~2K tokens│   │
│  │ Agent persona, rules, capabilities                   │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │ INSTRUCTIONS / SKILLS                      ~3K tokens│   │
│  │ Task-specific guidelines, domain knowledge           │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │ TOOL DEFINITIONS                           ~4K tokens│   │
│  │ Available tools with JSON schemas                    │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │ RETRIEVED CONTEXT (RAG)                   ~10K tokens│   │
│  │ Relevant documents, code files                       │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │ CONVERSATION HISTORY (summarized)          ~5K tokens│   │
│  │ Past interactions, summarized older turns            │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │ RECENT MESSAGES (full detail)              ~5K tokens│   │
│  │ Last 3-5 turns with full content                     │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │ CURRENT TASK CONTEXT                      ~10K tokens│   │
│  │ Code being edited, error logs, test results          │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │ ░░░░░░░ RESERVED FOR OUTPUT ░░░░░░░░     ~8K tokens │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  💡 Every token matters! Irrelevant context = worse results │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔑 The 7 Principles of Context Engineering

### 1. Right Information, Right Time
Don't dump everything in. **Dynamically select** what's relevant for this specific request.

```python
# ❌ Bad: Static, everything-in-the-prompt approach
system_prompt = ALL_DOCS + ALL_TOOLS + ALL_HISTORY  # Bloated!

# ✅ Good: Dynamic context selection
context = select_relevant_context(
    user_query=query,
    available_docs=search_index,
    conversation_state=state,
    max_tokens=10000,
)
```

### 2. Summarize Aggressively
Old conversation turns should be **summarized**, not kept verbatim.

```python
# ❌ Bad: Keep entire history
messages = all_messages_since_start  # Grows without bound!

# ✅ Good: Summarize + Keep Recent
messages = [
    summary_of_old_turns,    # Compressed history
    *last_5_messages,         # Recent full detail
    current_message,          # Current request
]
```

### 3. Layer Your Context (Priority System)

```
Priority 1 (MUST HAVE):  System prompt, current query, relevant tools
Priority 2 (IMPORTANT):  Retrieved docs, recent conversation
Priority 3 (NICE TO HAVE): User preferences, older history
Priority 4 (DROP FIRST):  Examples, verbose descriptions
```

### 4. Separate Concerns into Different Contexts
Instead of one massive prompt, use **different agents or calls** for different concerns.

### 5. Structure Over Prose
Use markdown headers, XML tags, or JSON — structured context is easier for models to parse.

```python
# ❌ Bad: Wall of text
context = "The user is Alice she likes Python and she previously asked about..."

# ✅ Good: Structured
context = """
<user_profile>
  Name: Alice
  Preferences: Python, dark mode, concise answers
</user_profile>

<current_task>
  Implement user authentication
</current_task>

<relevant_files>
  - auth.py (200 lines)
  - models.py (50 lines)
</relevant_files>
"""
```

### 6. Include "What Not to Do"
Negative examples are powerful context signals.

### 7. Test and Measure
Context engineering is empirical — measure output quality with different context strategies.

---

## 🏗️ Real-World Context Architecture

This is how GitHub Copilot, Cursor, and similar tools manage context:

```
┌─────────────────────────────────────────────────────────┐
│                    CONTEXT PIPELINE                       │
│                                                           │
│  User Types                                               │
│  a Request ─────┐                                        │
│                  ▼                                        │
│         ┌────────────────┐                               │
│         │ CONTEXT MANAGER│                               │
│         │                │                               │
│         │ 1. Parse intent│                               │
│         │ 2. Select what │                               │
│         │    to retrieve │                               │
│         └───┬──┬──┬──┬───┘                               │
│             │  │  │  │                                    │
│      ┌──────┘  │  │  └──────┐                            │
│      ▼         ▼  ▼         ▼                            │
│  ┌───────┐ ┌──────┐ ┌──────────┐ ┌──────────┐         │
│  │Memory │ │ RAG  │ │Open Files│ │ Tool     │          │
│  │Store  │ │Index │ │& Symbols │ │ Registry │          │
│  └───┬───┘ └──┬───┘ └────┬─────┘ └────┬─────┘         │
│      │        │          │             │                 │
│      └────────┴──────────┴─────────────┘                 │
│                     │                                     │
│                     ▼                                     │
│         ┌────────────────────┐                           │
│         │ CONTEXT ASSEMBLER  │                           │
│         │                    │                           │
│         │ 1. Rank by relevance│                          │
│         │ 2. Trim to fit     │                           │
│         │ 3. Structure output│                           │
│         └────────┬───────────┘                           │
│                  │                                        │
│                  ▼                                        │
│         ┌────────────────────┐                           │
│         │      LLM CALL      │                           │
│         └────────────────────┘                           │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

---

## 💻 Hands-On Examples

### Example 1: Context Window Management
See [examples/01_context_management.py](examples/01_context_management.py)

### Example 2: Dynamic Context Selection
See [examples/02_dynamic_context.py](examples/02_dynamic_context.py)

---

## 🧠 Key Takeaways

1. **Context Engineering > Prompt Engineering** — it's about the entire information environment
2. The context window is your **most precious resource** — every token must earn its place
3. **Summarize old context**, keep recent context detailed
4. **Structure matters** — use XML tags, markdown, or JSON
5. **Dynamic selection** — retrieve different context based on the query
6. This is the **#1 skill** for building production agentic AI systems

---

## 📚 Further Reading
- [Andrej Karpathy on Context Engineering](https://x.com/karpathy/status/1937476930718728604) — The term's origin
- [Building effective agents](https://www.anthropic.com/research/building-effective-agents) — Anthropic's guide
- [How to build an agent that can use tools](https://platform.openai.com/docs/guides/function-calling) — OpenAI guide

---

**← Previous:** [07: Multi-Agent Systems](../07-multi-agent-systems/README.md)  
**Next →** [09: MCP & Skills](../09-mcp-and-skills/README.md)
