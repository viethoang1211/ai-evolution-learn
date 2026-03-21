# Module 05: The ReAct Pattern — Reasoning + Acting

## 🎯 Learning Objectives
- Understand the ReAct paper and why it was revolutionary
- Implement a ReAct agent from scratch
- See how Thought → Action → Observation loops enable complex problem solving
- Understand why ReAct is the foundation of all modern AI agents

---

## 🔴 Pain Point: Function Calling Without Reasoning Is Blind

From Module 04, function calling lets LLMs use tools. But there's a problem:

```python
# User: "Find the cheapest flight from NYC to London next week, 
#        convert the price to EUR, and book it if under €500"

# Simple function calling approach:
# 1. Call search_flights() → gets results
# 2. Call convert_currency() → converts price
# 3. Call book_flight() → books it
# 
# But what if step 1 returns no results? 
# What if the conversion shows it's over €500?
# What if booking fails?
# 
# There's no REASONING between steps!
```

**The problem:** Basic function calling is **blind execution** — the LLM calls tools but doesn't reason about results before deciding the next step.

---

## 📖 The ReAct Framework (Yao et al., 2022)

**ReAct** = **Re**asoning + **Act**ing

The key insight: interleave **thinking** (reasoning traces) with **acting** (tool execution) in a loop.

```
┌─────────────────────────────────────────────────────┐
│                  ReAct LOOP                           │
│                                                       │
│   ┌──────────┐                                       │
│   │ THOUGHT  │  "I need to find flights first..."    │
│   └────┬─────┘                                       │
│        │                                              │
│        ▼                                              │
│   ┌──────────┐                                       │
│   │  ACTION  │  search_flights("NYC", "London")      │
│   └────┬─────┘                                       │
│        │                                              │
│        ▼                                              │
│   ┌──────────────┐                                   │
│   │ OBSERVATION  │  Found 3 flights: $450, $520, $380│
│   └────┬─────────┘                                   │
│        │                                              │
│        ▼                                              │
│   ┌──────────┐                                       │
│   │ THOUGHT  │  "Cheapest is $380. Let me convert   │
│   │          │   to EUR to check if under €500..."   │
│   └────┬─────┘                                       │
│        │                                              │
│        ▼                                              │
│   ┌──────────┐                                       │
│   │  ACTION  │  convert_currency(380, "USD", "EUR")  │
│   └────┬─────┘                                       │
│        │                                              │
│        ▼                                              │
│   ┌──────────────┐                                   │
│   │ OBSERVATION  │  380 USD = 348.60 EUR             │
│   └────┬─────────┘                                   │
│        │                                              │
│        ▼                                              │
│   ┌──────────┐                                       │
│   │ THOUGHT  │  "€348.60 < €500. I should book it!" │
│   └────┬─────┘                                       │
│        │                                              │
│        ▼                                              │
│   ┌──────────┐                                       │
│   │  ACTION  │  book_flight(flight_id="FL-003")      │
│   └────┬─────┘                                       │
│        │                                              │
│        ▼                                              │
│   ┌──────────┐                                       │
│   │  FINAL   │  "Done! Booked flight FL-003 for      │
│   │ ANSWER   │   $380 (€348.60), well under budget." │
│   └──────────┘                                       │
│                                                       │
└─────────────────────────────────────────────────────┘
```

### Why This Matters

| Without ReAct | With ReAct |
|---------------|------------|
| Blind tool execution | Reason before each action |
| No error handling | Can adapt when things fail |
| Fixed sequence | Dynamic planning |
| No intermediate decisions | Decides next step based on results |
| One-shot | Iterative refinement |

---

## 📊 ReAct vs. Other Approaches

```
┌──────────────────────────────────────────────────────────────┐
│                                                               │
│  "Standard" LLM       Reasoning Only      Acting Only         │
│  (No tools)           (Chain-of-Thought)  (Function Calling)  │
│                                                               │
│  Think → Answer       Think → Think →     Act → Act →         │
│                       Think → Answer      Act → Answer        │
│                                                               │
│  ❌ Can't act         ❌ Can't verify     ❌ Can't reason     │
│  ❌ Hallucinates      ❌ Hallucinates     ❌ Blind execution  │
│                                                               │
│                     ReAct (Combined)                          │
│                                                               │
│              Think → Act → Observe →                          │
│              Think → Act → Observe →                          │
│              Think → Answer                                   │
│                                                               │
│              ✅ Reasons about results                         │
│              ✅ Takes real actions                             │
│              ✅ Self-corrects                                  │
│              ✅ Grounds in observations                        │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## 🔴 ReAct Limitations

### 1. Single Agent — No Collaboration
ReAct gives us one agent that reasons and acts. But complex tasks need **multiple specialized agents** working together.
→ **Solved by: Multi-Agent Systems (Module 07)**

### 2. Context Grows Quickly
Each Thought + Action + Observation adds tokens. Long reasoning chains can exceed context limits.
→ **Solved by: Context Engineering (Module 08)**

### 3. Tool Discovery
The agent only knows about tools defined in its prompt. How does it discover new capabilities?
→ **Solved by: MCP Protocol (Module 09)**

---

## 💻 Hands-On Examples

### Example 1: ReAct Agent from Scratch
See [examples/01_react_agent.py](examples/01_react_agent.py)

### Example 2: ReAct with Error Recovery
See [examples/02_react_error_recovery.py](examples/02_react_error_recovery.py)

---

## 🧠 Key Takeaways

1. **ReAct** = Reasoning (thinking) + Acting (tool use) in an interleaved loop
2. The **Thought → Action → Observation** cycle enables multi-step problem solving
3. ReAct agents can **adapt** plans based on results and **recover** from errors
4. This is the **foundational pattern** behind every modern AI agent
5. ReAct is the bridge from "LLM with tools" to "autonomous AI agent"

---

## 📚 Further Reading
- [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) — The original paper
- [Toolformer](https://arxiv.org/abs/2302.04761) — Teaching LLMs to use tools
- [LangChain ReAct Agent](https://python.langchain.com/docs/modules/agents/) — Popular implementation

---

**← Previous:** [04: Function Calling & Tools](../04-function-calling-tools/README.md)  
**Next →** [06: Agentic AI Basics](../06-agentic-ai-basics/README.md)
