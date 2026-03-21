# Module 04: Function Calling & Tools — LLMs That Can Act

## 🎯 Learning Objectives
- Understand why function calling / tool use was invented
- Implement LLM ↔ Tool integration from scratch
- Know the difference between function calling and agentic tool use
- See how this enabled the leap from "chatbot" to "assistant"

---

## 🔴 Pain Point: LLMs Can Think But Can't Do

From previous modules:
- LLMs can **generate text** (Module 01)
- Prompts can **guide** the output (Module 02)  
- RAG can **ground** answers in documents (Module 03)

But none of these let an LLM **take actions in the real world**.

```python
# User: "What's the weather in Tokyo right now?"
# LLM:  "I don't have access to real-time weather data."  ← Useless!

# User: "Send an email to bob@company.com about the meeting"
# LLM:  "Here's a draft email you could send..."  ← Can't actually send it!

# User: "Create a JIRA ticket for this bug"
# LLM:  "You can create a JIRA ticket by going to..."  ← Doesn't do it!
```

**The breakthrough (June 2023):** OpenAI introduced **Function Calling** — a way for LLMs to say "I need to call this function with these arguments" instead of generating text.

---

## 📖 How Function Calling Works

```
┌──────────────────────────────────────────────────────────────┐
│                  FUNCTION CALLING FLOW                         │
│                                                               │
│  ┌──────┐   "What's the weather    ┌─────────┐               │
│  │ User │──── in Tokyo?"──────────▶│   LLM   │               │
│  └──────┘                          └────┬────┘               │
│                                         │                     │
│                          Instead of answering directly,       │
│                          the LLM returns a FUNCTION CALL:     │
│                                         │                     │
│                                         ▼                     │
│                          ┌──────────────────────┐            │
│                          │ get_weather(          │            │
│                          │   city="Tokyo"        │            │
│                          │ )                     │            │
│                          └──────────┬───────────┘            │
│                                     │                         │
│                          YOUR CODE executes the function      │
│                                     │                         │
│                                     ▼                         │
│                          ┌──────────────────────┐            │
│                          │ Result: {"temp": 22,  │            │
│                          │  "condition": "sunny"} │            │
│                          └──────────┬───────────┘            │
│                                     │                         │
│                          Feed result back to LLM              │
│                                     │                         │
│                                     ▼                         │
│                          ┌──────────────────────┐            │
│                          │ "The weather in       │            │
│  ┌──────┐               │  Tokyo is 22°C and    │            │
│  │ User │◀──────────────│  sunny today!"         │            │
│  └──────┘               └──────────────────────┘            │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

### The Key Insight

The LLM doesn't actually execute functions — it **decides which function to call and with what arguments**. Your application code does the actual execution. This is a critical safety boundary.

```
LLM's job:    Decide WHAT to call and with WHAT parameters
Your code:    Actually EXECUTE the function and return results
LLM's job:    Interpret the results and respond to the user
```

---

## 📊 Tool Definition Schema

Tools are defined with JSON Schema so the LLM knows what's available:

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name, e.g. 'Tokyo'"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "Temperature unit"
                    }
                },
                "required": ["city"]
            }
        }
    }
]
```

---

## 🔄 The Evolution: Function Calling → Tool Use → Agents

```
2023 Jun   Function Calling (OpenAI)
           └── Single function, single call
           
2023 Nov   Parallel Function Calling
           └── Multiple functions in one turn
           
2024       Tool Use (industry standard term)
           └── Functions + code interpreter + file access
           
2025       Agentic Tool Use
           └── LLM decides WHEN and WHICH tools to use in a loop
           └── This is the ReAct pattern (Module 05)
```

---

## 🔴 Limitations of Simple Function Calling

### 1. Single-Turn Only
The basic pattern is: User asks → LLM calls one tool → Returns answer. No multi-step reasoning.

### 2. No Planning
The LLM can't say "First I'll search, then I'll calculate, then I'll update." It's one step.

### 3. No Error Recovery
If a tool call fails, the basic pattern doesn't retry or try alternatives.

> **These limitations led to the ReAct pattern (Module 05) and full Agentic AI (Module 06).**

---

## 💻 Hands-On Examples

### Example 1: Basic Function Calling
See [examples/01_basic_function_calling.py](examples/01_basic_function_calling.py)

### Example 2: Multi-Tool Assistant
See [examples/02_multi_tool_assistant.py](examples/02_multi_tool_assistant.py)

---

## 🧠 Key Takeaways

1. **Function calling** lets LLMs trigger real-world actions through your code
2. The LLM **decides** what to call; **your code** executes it (safety boundary)
3. Tools are defined via **JSON Schema** — the LLM reads the schema to understand capabilities
4. This was the **first step** toward agentic AI — letting LLMs interact with the world
5. Simple function calling is **single-turn** — ReAct and agents add multi-step reasoning

---

**← Previous:** [03: RAG Pattern](../03-rag-pattern/README.md)  
**Next →** [05: ReAct Pattern](../05-react-pattern/README.md)
