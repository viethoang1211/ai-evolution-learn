# Module 02: Prompt Engineering — Making LLMs Actually Useful

## 🎯 Learning Objectives
- Understand why prompt engineering emerged as a discipline
- Master key prompting techniques: zero-shot, few-shot, chain-of-thought, system prompts
- See the limitations that eventually led to "Context Engineering"

---

## 🔴 Pain Point: Raw LLMs Give Inconsistent, Low-Quality Outputs

From Module 01, we know LLMs are text prediction engines. But **how you ask** dramatically changes **what you get**.

```python
# Bad prompt → Bad result
response = llm("Write code for sorting")
# Could return anything: pseudocode, Python, Java, bubble sort, quicksort...

# Good prompt → Good result
response = llm("""Write a Python function that:
- Takes a list of integers as input
- Returns the list sorted in ascending order
- Uses the merge sort algorithm
- Includes type hints and a docstring
""")
# Returns exactly what you need
```

**The pain point:** Engineers realized that getting good outputs from LLMs required a specific skill — crafting the right prompts. This became its own discipline: **Prompt Engineering**.

---

## 📖 The Evolution of Prompting Techniques

### Level 1: Zero-Shot Prompting (Just ask)

```
Prompt: "Translate 'Hello World' to French"
Output: "Bonjour le Monde"
```

No examples needed. Works for simple, well-defined tasks.

### Level 2: Few-Shot Prompting (Show examples)

**Pain point:** Zero-shot fails on complex or ambiguous tasks.

```
Prompt:
  Classify the sentiment of these reviews:

  Review: "This product is amazing!" → Positive
  Review: "Terrible quality, broke in a day" → Negative
  Review: "It's okay, nothing special" → Neutral

  Review: "I absolutely love this, best purchase ever!" → 
  
Output: "Positive"
```

The model learns the task pattern from examples in the prompt.

### Level 3: Chain-of-Thought (Think step by step)

**Pain point:** LLMs fail at complex reasoning tasks even with examples.

```
# Without Chain-of-Thought
Q: "If a store has 23 apples and sells 7, then receives 15 more, 
    then sells half of what's left, how many remain?"
A: "15.5" ← WRONG

# With Chain-of-Thought
Q: "... Think step by step."
A: "Let me work through this:
    1. Start with 23 apples
    2. Sell 7: 23 - 7 = 16
    3. Receive 15: 16 + 15 = 31
    4. Sell half: 31 / 2 = 15.5
    Answer: 15.5 apples, but since we can't have half an apple,
    this means 15 apples remain and half was left unsold."
```

### Level 4: System Prompts (Define the AI's persona)

**Pain point:** Every user message had to repeat the context and rules.

```python
messages = [
    {
        "role": "system",
        "content": """You are a senior Python developer who:
        - Always uses type hints
        - Follows PEP 8 style guide
        - Writes comprehensive docstrings
        - Suggests test cases for every function
        - Flags potential security issues"""
    },
    {
        "role": "user",
        "content": "Write a function to validate email addresses"
    }
]
```

### Level 5: Structured Output (JSON Mode)

**Pain point:** LLMs return free-form text, but applications need structured data.

```python
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{
        "role": "user",
        "content": "Extract entities from: 'Apple CEO Tim Cook announced iPhone 16 in Cupertino'"
    }],
    response_format={"type": "json_object"}
)
# Returns: {"entities": [{"name": "Apple", "type": "ORG"}, ...]}
```

---

## 📊 Prompt Engineering Patterns — Complete Reference

```
┌────────────────────────────────────────────────────────┐
│              PROMPT ENGINEERING PATTERNS                │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1. ROLE PATTERN                                       │
│     "You are a {role} who {specialization}"            │
│                                                        │
│  2. TEMPLATE PATTERN                                   │
│     "Given {input}, produce {output} in {format}"      │
│                                                        │
│  3. CHAIN-OF-THOUGHT                                   │
│     "Think step by step before answering"              │
│                                                        │
│  4. FEW-SHOT                                           │
│     "Here are examples: ... Now do this: ..."          │
│                                                        │
│  5. SELF-CONSISTENCY                                   │
│     Ask N times, take majority vote                    │
│                                                        │
│  6. TREE-OF-THOUGHT                                    │
│     Explore multiple reasoning paths                   │
│                                                        │
│  7. ReAct (preview — Module 05)                        │
│     Thought → Action → Observation → Repeat            │
│                                                        │
└────────────────────────────────────────────────────────┘
```

---

## 🔴 The Limits of Prompt Engineering

Even the best prompts can't solve fundamental problems:

| Problem | Why Prompts Can't Fix It |
|---------|-------------------------|
| No real-time data | No matter how clever the prompt, the model can't access the internet |
| Hallucination | Better prompts reduce but can't eliminate fabrication |
| No actions | Prompts can't make the model send emails or query databases |
| Knowledge limits | The training cutoff still applies |
| Token limits | Long prompts eat into the available context window |

> **This realization led to the next evolution: giving LLMs access to external knowledge (RAG — Module 03) and tools (Module 04).**

---

## 💻 Hands-On Examples

### Example 1: Prompting Techniques Comparison
See [examples/01_prompting_techniques.py](examples/01_prompting_techniques.py)

### Example 2: System Prompts and Personas
See [examples/02_system_prompts.py](examples/02_system_prompts.py)

### Example 3: Structured Output
See [examples/03_structured_output.py](examples/03_structured_output.py)

---

## 🧠 Key Takeaways

1. **Prompt engineering** emerged because LLM output quality is highly sensitive to input phrasing
2. **Few-shot learning** lets models learn from examples without fine-tuning
3. **Chain-of-thought** unlocks reasoning by making the model show its work
4. **System prompts** provide persistent context and persona
5. Prompt engineering is **necessary but insufficient** — it can't overcome fundamental LLM limitations

---

**← Previous:** [01: Foundation LLMs](../01-foundation-llms/README.md)  
**Next →** [03: RAG — Retrieval-Augmented Generation](../03-rag-pattern/README.md)
