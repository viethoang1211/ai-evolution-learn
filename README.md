# 🧠 The Evolution of AI: From LLMs to Modern Agentic AI

A comprehensive English lecture series covering the complete evolution of AI — from basic Large Language Models to modern agentic AI systems. Each module explains the **pain point** that drove the innovation, with **hands-on code examples** you can run.

---

## 📋 Course Overview

```
    The AI Evolution Timeline
    
    LLM ──▶ Prompting ──▶ RAG ──▶ Tools ──▶ ReAct ──▶ Agents ──▶ Multi-Agent ──▶ Context Eng. ──▶ MCP ──▶ Modern AI
    
    Module:  01      02       03     04      05       06         07              08              09       10
```

---

## 📚 Modules

| # | Module | Pain Point Solved | Key Concepts |
|---|--------|-------------------|-------------|
| 01 | [**Foundation LLMs**](01-foundation-llms/README.md) | Understanding the base technology | Transformers, tokens, emergent abilities |
| 02 | [**Prompt Engineering**](02-prompt-engineering/README.md) | Inconsistent LLM outputs | Zero-shot, few-shot, CoT, system prompts |
| 03 | [**RAG Pattern**](03-rag-pattern/README.md) | Hallucination, knowledge cutoff | Embeddings, vector search, retrieval |
| 04 | [**Function Calling & Tools**](04-function-calling-tools/README.md) | LLMs can't take actions | Tool schemas, function execution |
| 05 | [**ReAct Pattern**](05-react-pattern/README.md) | No reasoning between actions | Thought → Action → Observation loop |
| 06 | [**Agentic AI Basics**](06-agentic-ai-basics/README.md) | Reactive, not proactive | Planning, memory, reflection, autonomy |
| 07 | [**Multi-Agent Systems**](07-multi-agent-systems/README.md) | Single agent bottleneck | Orchestrator, pipeline, debate, swarm |
| 08 | [**Context Engineering**](08-context-engineering/README.md) | Context window chaos | Dynamic selection, summarization, priority |
| 09 | [**MCP & Skills**](09-mcp-and-skills/README.md) | N×M integration problem | Standard protocol, plug-and-play tools |
| 10 | [**Modern Agentic AI**](10-modern-agentic-ai/README.md) | Putting it all together | Complete system architecture |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- An OpenAI API key (for running examples)

### Setup

```bash
# Clone the repository
git clone <repo-url>
cd ai-evolution-learn

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Set your API key (Option A: OpenAI)
export OPENAI_API_KEY="your-key-here"

# Or use Azure OpenAI (Option B):
export USE_AZURE_OPENAI=true
export AZURE_OPENAI_API_KEY="your-azure-key"
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
export AZURE_OPENAI_API_VERSION="2024-12-01-preview"
export AZURE_OPENAI_DEPLOYMENT="gpt-4o-test"                        # chat model deployment
export AZURE_OPENAI_EMBEDDING_DEPLOYMENT="text-embedding-3-small"   # embedding deployment (Module 03)
```

### Running Examples

Each module has an `examples/` directory with runnable Python scripts:

```bash
# Run any example
python 01-foundation-llms/examples/01_basic_llm_call.py
python 05-react-pattern/examples/01_react_agent.py
python 10-modern-agentic-ai/examples/01_mini_agent.py
```

---

## 🗺️ Learning Path

### Recommended Order (Sequential)
Follow modules 01 → 10 in order. Each builds on the previous.

### Quick Path (If You Have Experience)
- If you know LLMs & prompting: Start at **Module 03 (RAG)**
- If you know RAG & tools: Start at **Module 05 (ReAct)**
- If you want cutting-edge only: Start at **Module 08 (Context Engineering)**

### By Interest Area
- **Building chatbots**: Modules 01–03
- **Building AI assistants**: Modules 04–06
- **Building AI agent systems**: Modules 07–10
- **Understanding MCP/Copilot**: Modules 09–10

---

## 📊 The Story Arc: Pain Points → Innovations

```
Pain: "LLMs give random outputs"
  └─→ Innovation: Prompt Engineering (Module 02)

Pain: "LLMs hallucinate and don't know my data"
  └─→ Innovation: RAG (Module 03)

Pain: "LLMs can think but can't DO anything"
  └─→ Innovation: Function Calling / Tools (Module 04)

Pain: "Tool use without reasoning is blind"
  └─→ Innovation: ReAct Pattern (Module 05)

Pain: "Agents are reactive, not proactive"
  └─→ Innovation: Agentic AI with Planning & Memory (Module 06)

Pain: "One agent can't handle complex tasks"
  └─→ Innovation: Multi-Agent Systems (Module 07)

Pain: "Too much information, too little context window"
  └─→ Innovation: Context Engineering (Module 08)

Pain: "Every AI tool needs custom integrations"
  └─→ Innovation: MCP Protocol & Skills (Module 09)

Result: Modern Agentic AI that plans, reasons, acts, and learns (Module 10)
```

---

## 🛠️ Tech Stack Used

| Technology | Purpose |
|-----------|---------|
| Python 3.11+ | All examples |
| OpenAI API | LLM calls (GPT-4o-mini) |
| Azure OpenAI | Alternative LLM backend (same code, just set env vars) |
| NumPy | Vector operations (RAG) |

> **Note:** Examples use `gpt-4o-mini` for cost-efficiency. You can swap to any model (Claude, Gemini, local models) by changing the API client.

---

## 📝 License

This course material is open source. Use it freely for learning, teaching, and building.

---

**Start your journey →** [Module 01: Foundation LLMs](01-foundation-llms/README.md)
