# Module 07: Multi-Agent Systems — Specialization & Collaboration

## 🎯 Learning Objectives
- Understand why single agents hit limits on complex tasks
- Learn multi-agent patterns: orchestrator, pipeline, debate, swarm
- Build a multi-agent system from scratch
- Know the key frameworks: CrewAI, AutoGen, LangGraph, OpenAI Swarm

---

## 🔴 Pain Point: One Agent Can't Do Everything Well

From Module 06, we have autonomous agents. But as tasks get complex:

```
Single Agent attempting a complex task:

"Build a full-stack web app with user authentication, 
 deploy it to AWS, and write documentation."

Problems:
❌ System prompt becomes enormous (trying to define all skills)
❌ Context window fills up with mixed concerns
❌ No specialization — jack of all trades, master of none
❌ One error can derail the entire multi-step process
❌ Can't parallelize independent sub-tasks
```

**The solution:** Instead of one "super agent," use **multiple specialized agents** that collaborate — just like a development team.

---

## 📖 Multi-Agent Patterns

### Pattern 1: Orchestrator (Manager Agent)

```
┌─────────────────────────────────────────────────┐
│               ORCHESTRATOR PATTERN                │
│                                                   │
│          ┌──────────────────┐                    │
│          │   ORCHESTRATOR   │                    │
│          │   (Manager)      │                    │
│          │                  │                    │
│          │  Breaks task     │                    │
│          │  into subtasks   │                    │
│          │  and delegates   │                    │
│          └───┬───┬───┬──────┘                    │
│              │   │   │                            │
│       ┌──────┘   │   └──────┐                    │
│       ▼          ▼          ▼                    │
│  ┌─────────┐ ┌────────┐ ┌─────────┐            │
│  │ CODER   │ │ TESTER │ │ WRITER  │            │
│  │ Agent   │ │ Agent  │ │ Agent   │            │
│  │         │ │        │ │         │            │
│  │ Writes  │ │ Writes │ │ Writes  │            │
│  │ code    │ │ tests  │ │ docs    │            │
│  └─────────┘ └────────┘ └─────────┘            │
│                                                   │
│  Used by: CrewAI, OpenAI Agents SDK (handoffs)   │
└─────────────────────────────────────────────────┘
```

### Pattern 2: Pipeline (Sequential Handoff)

```
┌─────────────────────────────────────────────────┐
│               PIPELINE PATTERN                    │
│                                                   │
│  ┌─────────┐   ┌──────────┐   ┌──────────┐     │
│  │ PLANNER │──▶│ EXECUTOR │──▶│ REVIEWER │     │
│  │         │   │          │   │          │     │
│  │ Creates │   │ Carries  │   │ Checks   │     │
│  │ plan    │   │ out plan │   │ quality  │     │
│  └─────────┘   └──────────┘   └──────────┘     │
│                                     │            │
│                                     ▼            │
│                              ┌──────────┐        │
│                              │ Pass or  │        │
│                              │ send back│        │
│                              └──────────┘        │
│                                                   │
│  Used by: Software review pipelines              │
└─────────────────────────────────────────────────┘
```

### Pattern 3: Debate (Adversarial Collaboration)

```
┌─────────────────────────────────────────────────┐
│               DEBATE PATTERN                      │
│                                                   │
│     ┌──────────┐       ┌──────────┐             │
│     │ AGENT A  │◀─────▶│ AGENT B  │             │
│     │          │       │          │             │
│     │ Proposes │       │ Critiques│             │
│     │ solution │       │ proposes │             │
│     │          │       │ better   │             │
│     └────┬─────┘       └────┬─────┘             │
│          │                  │                    │
│          └──────┬───────────┘                    │
│                 ▼                                 │
│          ┌──────────┐                            │
│          │  JUDGE   │                            │
│          │  Agent   │                            │
│          │          │                            │
│          │ Picks    │                            │
│          │ best     │                            │
│          └──────────┘                            │
│                                                   │
│  Used by: Constitutional AI, red-teaming         │
└─────────────────────────────────────────────────┘
```

### Pattern 4: Swarm (Dynamic Routing)

```
┌─────────────────────────────────────────────────┐
│               SWARM PATTERN                       │
│                                                   │
│     User message arrives                         │
│              │                                    │
│              ▼                                    │
│     ┌────────────────┐                           │
│     │  TRIAGE AGENT  │                           │
│     │  Routes to the │                           │
│     │  right expert  │                           │
│     └───┬────┬────┬──┘                           │
│         │    │    │                               │
│    ┌────┘    │    └────┐                         │
│    ▼         ▼         ▼                         │
│  ┌──────┐ ┌──────┐ ┌──────┐                    │
│  │Sales │ │Tech  │ │Bill  │                    │
│  │Agent │ │Agent │ │Agent │                    │
│  └──────┘ └──────┘ └──────┘                    │
│                                                   │
│  Agents can HAND OFF to each other              │
│  Used by: OpenAI Swarm, customer support bots   │
└─────────────────────────────────────────────────┘
```

---

## 📊 When to Use Multi-Agent vs Single Agent

| Scenario | Single Agent | Multi-Agent |
|----------|-------------|-------------|
| Simple Q&A | ✅ | Overkill |
| Code generation | ✅ | ✅ (coder + reviewer) |
| Full project development | ❌ Too complex | ✅ |
| Customer support routing | ❌ | ✅ Swarm pattern |
| Content review pipeline | ❌ | ✅ Pipeline pattern |
| Research & analysis | ❌ | ✅ Debate pattern |

---

## 💻 Hands-On Examples

### Example 1: Orchestrator Multi-Agent System
See [examples/01_orchestrator_agents.py](examples/01_orchestrator_agents.py)

### Example 2: Code Review Pipeline
See [examples/02_code_review_pipeline.py](examples/02_code_review_pipeline.py)

---

## 🧠 Key Takeaways

1. **Multi-agent systems** split complex tasks among specialized agents
2. **Orchestrator pattern** uses a manager agent to delegate sub-tasks
3. **Pipeline pattern** chains agents in sequence (plan → execute → review)
4. **Debate pattern** uses adversarial agents to improve quality
5. **Swarm pattern** routes requests to the right specialist dynamically
6. Each agent has a **focused system prompt** — specialization beats generalization

---

**← Previous:** [06: Agentic AI Basics](../06-agentic-ai-basics/README.md)  
**Next →** [08: Context Engineering](../08-context-engineering/README.md)
