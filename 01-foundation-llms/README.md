# Module 01: Foundation — Large Language Models (LLMs)

## 🎯 Learning Objectives
- Understand what LLMs are and how they work at a high level
- Know the key milestones: GPT-2 → GPT-3 → ChatGPT → GPT-4 → Claude/Gemini
- Understand the core limitation: **LLMs are stateless text completion engines**

---

## 📖 The Story: From Text Prediction to Intelligence

### What is an LLM?

A Large Language Model is essentially a **probability machine** — given a sequence of tokens (words/sub-words), it predicts the most likely next token.

```
Input:  "The capital of France is"
Output: " Paris" (with 95% probability)
```

That's it. Everything else — conversations, coding, reasoning — emerges from this simple mechanism scaled to billions of parameters trained on trillions of tokens.

### The Timeline

| Year | Model | Parameters | Key Breakthrough |
|------|-------|-----------|-----------------|
| 2018 | GPT-1 | 117M | Transfer learning for NLP |
| 2019 | GPT-2 | 1.5B | "Too dangerous to release" — coherent text generation |
| 2020 | GPT-3 | 175B | Few-shot learning — no fine-tuning needed |
| 2022 | ChatGPT | ~175B | RLHF — aligned with human intentions |
| 2023 | GPT-4 | ~1.8T (est.) | Multimodal, reasoning leap |
| 2023 | Claude 2 | Unknown | Long context (100K tokens), safety focus |
| 2024 | Claude 3.5 | Unknown | Artifacts, computer use |
| 2024 | GPT-4o | Unknown | Omni-modal (text, image, audio, video) |
| 2025 | Claude Opus 4 | Unknown | Extended thinking, agentic capabilities |

### The Core Architecture: Transformer

Every modern LLM is built on the **Transformer** architecture (Vaswani et al., 2017 — "Attention Is All You Need").

```
┌─────────────────────────────────┐
│         OUTPUT TOKENS           │
│    "Paris is a beautiful..."    │
└──────────────┬──────────────────┘
               │
┌──────────────▼──────────────────┐
│      DECODER LAYERS (×N)        │
│  ┌───────────────────────────┐  │
│  │   Self-Attention          │  │
│  │   (What to focus on?)     │  │
│  ├───────────────────────────┤  │
│  │   Feed-Forward Network    │  │
│  │   (Transform the info)    │  │
│  └───────────────────────────┘  │
└──────────────┬──────────────────┘
               │
┌──────────────▼──────────────────┐
│       INPUT EMBEDDINGS          │
│  "The capital of France is"     │
└─────────────────────────────────┘
```

### The Key Insight: Emergent Abilities

As models scale up, they don't just get better at text prediction — they develop **emergent abilities**:

- **Few-shot learning** (GPT-3): Learn from examples in the prompt
- **Chain-of-thought reasoning** (>100B params): Step-by-step logical thinking
- **Code generation**: Understanding and writing programming languages
- **Instruction following**: Understanding what humans want

---

## 🔴 Pain Points of Raw LLMs

These pain points drove every subsequent innovation in this course:

### 1. **No Memory** — Stateless by Design
Each API call is independent. The model doesn't remember previous conversations.

```python
# Call 1
response = llm("My name is Alice")  # "Nice to meet you, Alice!"

# Call 2 — completely independent!
response = llm("What's my name?")   # "I don't know your name."
```

### 2. **Knowledge Cutoff** — Frozen in Time
LLMs only know what was in their training data. They can't access real-time information.

```python
response = llm("What's the current stock price of Apple?")
# "I don't have access to real-time data. As of my last update..."
```

### 3. **Hallucination** — Confident but Wrong
LLMs generate plausible-sounding but factually incorrect information.

```python
response = llm("Tell me about the research paper 'Quantum Neural Oscillations' by Dr. Smith 2024")
# Will confidently describe a paper that doesn't exist!
```

### 4. **No Actions** — Can Only Generate Text
LLMs can tell you how to book a flight, but they can't actually book it.

```python
response = llm("Book me a flight from NYC to London")
# "Sure! Here are the steps to book a flight..."
# But no flight is actually booked!
```

### 5. **Context Window Limit** — Can't Read Everything
Even modern models have limits (4K → 8K → 128K → 200K tokens), but enterprise codebases have millions of lines.

---

## 💻 Hands-On Examples

### Example 1: Basic LLM API Call

See [examples/01_basic_llm_call.py](examples/01_basic_llm_call.py)

### Example 2: Demonstrating Statelessness

See [examples/02_stateless_demo.py](examples/02_stateless_demo.py)

### Example 3: Hallucination Demo

See [examples/03_hallucination_demo.py](examples/03_hallucination_demo.py)

---

## 🧠 Key Takeaways

1. LLMs are **incredibly powerful text generators** but have fundamental limitations
2. They are **stateless** — no memory between calls
3. They **hallucinate** — generate plausible but wrong information
4. They **can't take actions** — only generate text
5. They have a **knowledge cutoff** — no real-time information

> **The entire evolution from LLMs to Agentic AI is the story of solving these pain points one by one.**

---

## 📚 Further Reading
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) — The Transformer paper
- [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165) — GPT-3 paper
- [Training Language Models to Follow Instructions](https://arxiv.org/abs/2203.02155) — InstructGPT / RLHF

---

**Next Module →** [02: Prompt Engineering — Making LLMs Useful](../02-prompt-engineering/README.md)
