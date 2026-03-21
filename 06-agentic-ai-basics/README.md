# Module 06: Agentic AI — From Chatbot to Autonomous Agent

## 🎯 Learning Objectives
- Define what makes an AI system "agentic"
- Understand the spectrum from chatbot to fully autonomous agent
- Build a complete agentic system with planning, execution, and reflection
- Know the key frameworks: LangChain, CrewAI, AutoGen, OpenAI Agents SDK

---

## 🔴 Pain Point: ReAct Agents Are Reactive, Not Proactive

From Module 05, ReAct gives us the Thought → Action → Observation loop. But:

```
ReAct Agent: "I received a question. Let me use tools to answer it."
             → Reactive: Responds to a single question, then stops.

Agentic AI:  "I have a GOAL. Let me PLAN a strategy, EXECUTE steps,
              REFLECT on progress, and ADAPT my approach until done."
             → Proactive: Pursues goals autonomously across many steps.
```

**The evolution:**

```
Chatbot → Tool-Using LLM → ReAct Agent → Agentic AI
                                              │
                                              ├── Planning
                                              ├── Memory (short + long term)
                                              ├── Self-reflection
                                              ├── Error recovery
                                              └── Goal-oriented autonomy
```

---

## 📖 What Makes AI "Agentic"?

### The Agentic Spectrum

```
┌────────────────────────────────────────────────────────────┐
│                   THE AGENTIC SPECTRUM                      │
│                                                             │
│  Level 0     Level 1        Level 2         Level 3         │
│  CHATBOT     TOOL USER      ReAct AGENT     AGENTIC AI     │
│                                                             │
│  Q&A only    Can call       Reason+Act      Plan+Execute   │
│              APIs           in a loop       +Reflect+Adapt  │
│                                                             │
│  No tools    Fixed tools    Dynamic tool    Autonomous      │
│                             selection       goal pursuit    │
│                                                             │
│  Stateless   Single-turn    Multi-step      Multi-session   │
│              tool use       within query    memory+goals    │
│                                                             │
│  ChatGPT     GPT + Plugins  ReAct Agent     Devin, Copilot │
│  (2022)      (2023)         (2023)          Agent (2025)    │
│                                                             │
│  ◀──────────── Increasing Autonomy ──────────────────────▶ │
└────────────────────────────────────────────────────────────┘
```

### The 5 Properties of Agentic AI

| Property | Description | Example |
|----------|-------------|---------|
| **Planning** | Break goals into sub-tasks | "To deploy this feature, I need to: 1) write code, 2) write tests, 3) create PR, 4) request review" |
| **Tool Use** | Interact with external systems | Read files, run commands, call APIs |
| **Memory** | Retain context across interactions | Remember user preferences, past decisions |
| **Reflection** | Evaluate own outputs and progress | "My test failed — let me analyze the error and try a different approach" |
| **Autonomy** | Act without step-by-step human guidance | Execute a multi-step plan independently |

---

## 📊 Agent Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    AGENTIC AI SYSTEM                      │
│                                                           │
│  ┌──────────────────────────────────────────────────┐    │
│  │                  AGENT CORE                       │    │
│  │                                                   │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────┐   │    │
│  │  │ PLANNER  │  │ EXECUTOR │  │  REFLECTOR    │   │    │
│  │  │          │  │          │  │              │   │    │
│  │  │ Break    │  │ Run      │  │ Evaluate     │   │    │
│  │  │ goal     │→ │ actions  │→ │ results      │   │    │
│  │  │ into     │  │ step by  │  │ and adapt    │   │    │
│  │  │ steps    │  │ step     │  │ plan         │   │    │
│  │  └──────────┘  └──────────┘  └──────────────┘   │    │
│  │       ▲              │              │             │    │
│  │       └──────────────┴──────────────┘             │    │
│  │              (Feedback Loop)                       │    │
│  └──────────────────────────────────────────────────┘    │
│           │              │              │                  │
│  ┌────────▼──┐  ┌───────▼───┐  ┌──────▼──────┐         │
│  │  MEMORY   │  │   TOOLS   │  │   CONTEXT    │         │
│  │           │  │           │  │              │         │
│  │ Short-term│  │ Search    │  │ System       │         │
│  │ Long-term │  │ Code exec │  │ prompt       │         │
│  │ Episodic  │  │ File I/O  │  │ User prefs   │         │
│  │           │  │ APIs      │  │ Domain rules │         │
│  └───────────┘  └───────────┘  └──────────────┘         │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

---

## 🔄 The Agent Loop (Enhanced ReAct)

```python
# Pseudocode for the agentic loop
while not goal_achieved and attempts < max_attempts:
    # 1. PLAN: What should I do next?
    plan = llm.plan(goal, current_state, memory)
    
    # 2. EXECUTE: Carry out the next step
    result = execute_action(plan.next_action)
    
    # 3. OBSERVE: What happened?
    observation = observe(result)
    
    # 4. REFLECT: Did it work? Should I change approach?
    reflection = llm.reflect(plan, observation)
    
    # 5. UPDATE: Store results, update plan
    memory.store(observation, reflection)
    
    if reflection.goal_achieved:
        break
    elif reflection.needs_replan:
        plan = llm.replan(goal, memory)
```

---

## 🔴 Pain Points Leading to Further Evolution

### 1. Single Agent Bottleneck
One agent doing everything is slow and error-prone for complex tasks.
→ **Solved by: Multi-Agent Systems (Module 07)**

### 2. Prompt/Context Bloat
As agents get more capable, their system prompts grow enormous.
→ **Solved by: Context Engineering (Module 08)**

### 3. Tool Integration Hell
Every agent needs custom tool integrations. No standardization.
→ **Solved by: MCP — Model Context Protocol (Module 09)**

---

## 💻 Hands-On Examples

### Example 1: Planning Agent
See [examples/01_planning_agent.py](examples/01_planning_agent.py)

### Example 2: Agent with Memory and Reflection
See [examples/02_agent_with_memory.py](examples/02_agent_with_memory.py)

---

## 🧠 Key Takeaways

1. **Agentic AI** = Planning + Tool Use + Memory + Reflection + Autonomy
2. It's a **spectrum** — from simple chatbots to fully autonomous agents
3. The **agent loop** extends ReAct with planning and reflection phases
4. Real agents need **error recovery** and the ability to **re-plan**
5. This is where modern coding assistants (Copilot, Cursor, Devin) operate

---

**← Previous:** [05: ReAct Pattern](../05-react-pattern/README.md)  
**Next →** [07: Multi-Agent Systems](../07-multi-agent-systems/README.md)
