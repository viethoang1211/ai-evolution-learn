# Module 03: RAG — Retrieval-Augmented Generation

## 🎯 Learning Objectives
- Understand why RAG was invented and what pain points it solves
- Build a complete RAG pipeline from scratch
- Know the key components: embedding, vector store, retrieval, generation
- Understand RAG's limitations that led to further innovations

---

## 🔴 Pain Point: LLMs Are Frozen in Time and Hallucinate

From Modules 01 and 02, we know:
- LLMs have a **knowledge cutoff** — they don't know about recent events
- LLMs **hallucinate** — they confidently generate false information
- LLMs can't access **your private data** — company docs, databases, internal wikis

**The question:** How do we ground LLMs in real, authoritative, up-to-date information?

**The answer:** Don't try to put everything into the model — **retrieve relevant information at query time** and inject it into the prompt.

---

## 📖 How RAG Works

```
┌─────────────────────────────────────────────────────────────────┐
│                      RAG PIPELINE                                │
│                                                                  │
│   ┌────────┐    ┌──────────┐    ┌──────────┐    ┌───────────┐  │
│   │  User  │───▶│ Embed    │───▶│ Vector   │───▶│ Retrieve  │  │
│   │ Query  │    │ Query    │    │ Search   │    │ Top-K     │  │
│   └────────┘    └──────────┘    └──────────┘    └─────┬─────┘  │
│                                                        │        │
│                                              ┌─────────▼──────┐ │
│   ┌────────┐    ┌──────────┐                │ Context Docs   │ │
│   │  LLM   │◀───│ Augmented│◀───────────────│ (Retrieved)    │ │
│   │Response│    │ Prompt   │                └────────────────┘ │
│   └────────┘    └──────────┘                                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Step-by-Step:

1. **Index Phase** (offline, one-time):
   - Split documents into chunks
   - Convert each chunk into a vector embedding
   - Store embeddings in a vector database

2. **Query Phase** (online, per-request):
   - Convert user question into a vector embedding
   - Find the most similar document chunks (cosine similarity)
   - Inject retrieved chunks into the prompt as context
   - LLM generates an answer **grounded in the retrieved documents**

### What Are Embeddings?

Embeddings are numerical representations of text where **semantic similarity** maps to **vector proximity**.

```
"king" → [0.2, 0.8, 0.1, ...]
"queen" → [0.3, 0.7, 0.1, ...]    ← Similar to "king"
"banana" → [0.9, 0.1, 0.5, ...]   ← Very different from "king"

cosine_similarity("king", "queen") = 0.95  ← High!
cosine_similarity("king", "banana") = 0.12 ← Low!
```

---

## 📊 RAG vs. Fine-Tuning

| Aspect | RAG | Fine-Tuning |
|--------|-----|-------------|
| **Data freshness** | ✅ Always current | ❌ Frozen at training time |
| **Setup cost** | Low (days) | High (weeks, GPUs) |
| **Transparency** | ✅ Can cite sources | ❌ Black box |
| **Accuracy** | High (from documents) | Variable |
| **Scalability** | ✅ Add docs anytime | ❌ Retrain needed |
| **Best for** | Knowledge Q&A, search | Style, behavior change |

---

## 🔴 RAG Limitations (Pain Points for Next Modules)

### 1. Passive — Can Only Read, Not Act
RAG can find information but can't take actions (send emails, update databases).
→ **Solved by: Tools / Function Calling (Module 04)**

### 2. One-Shot Retrieval — No Iterative Reasoning
RAG retrieves documents once and answers. It can't say "I need more info, let me search again."
→ **Solved by: ReAct Pattern (Module 05)**

### 3. Chunking Is Hard
Splitting documents into the right-sized chunks is an art. Too small = lost context. Too large = noise.

### 4. Embedding Quality Matters
If the embedding model doesn't understand domain-specific terms, retrieval quality drops.

---

## 💻 Hands-On Examples

### Example 1: Simple RAG from Scratch
See [examples/01_simple_rag.py](examples/01_simple_rag.py)

### Example 2: RAG vs. Pure LLM Comparison
See [examples/02_rag_vs_pure_llm.py](examples/02_rag_vs_pure_llm.py)

---

## 🧠 Key Takeaways

1. **RAG = Retrieve + Augment + Generate** — ground LLMs in real documents
2. Solves **hallucination** by providing authoritative source material
3. Solves **knowledge cutoff** by indexing up-to-date documents
4. Uses **vector embeddings** for semantic search (not keyword matching)
5. RAG is **read-only** — it can find info but can't take actions

---

**← Previous:** [02: Prompt Engineering](../02-prompt-engineering/README.md)  
**Next →** [04: Function Calling & Tools](../04-function-calling-tools/README.md)
