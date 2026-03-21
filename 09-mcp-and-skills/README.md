# Module 09: MCP (Model Context Protocol) & Skills — Standardizing AI Integration

## 🎯 Learning Objectives
- Understand why MCP was created and what problem it solves
- Know the MCP architecture: hosts, clients, servers
- Understand Skills as packaged domain knowledge
- See how MCP + Skills = plug-and-play AI capabilities

---

## 🔴 Pain Point: The Tool Integration Nightmare (N×M Problem)

From Modules 04-08, we've given agents tools, reasoning, and context. But in practice:

```
Before MCP — The N×M Problem:

Every AI app needs custom integrations for every service.

  AI Apps (N)              Services (M)
  ┌─────────┐           ┌─────────────┐
  │ ChatGPT │──custom──▶│   GitHub    │
  │         │──custom──▶│   Slack     │
  │         │──custom──▶│   Jira      │
  ├─────────┤           ├─────────────┤
  │ Claude  │──custom──▶│   GitHub    │
  │         │──custom──▶│   Slack     │
  │         │──custom──▶│   Jira      │
  ├─────────┤           ├─────────────┤
  │ Copilot │──custom──▶│   GitHub    │
  │         │──custom──▶│   Slack     │
  │         │──custom──▶│   Jira      │
  └─────────┘           └─────────────┘

  Total integrations needed: N × M = 3 × 3 = 9 custom implementations!
  For 10 apps × 20 services = 200 custom integrations! 😱
```

**The solution:** A **standard protocol** so any AI app can talk to any service through a common interface — like USB for AI.

```
After MCP — The N+M Solution:

  AI Apps (N)              MCP              Services (M)
  ┌─────────┐         ┌─────────┐       ┌─────────────┐
  │ ChatGPT │─────┐   │         │   ┌──▶│   GitHub    │
  ├─────────┤     │   │   MCP   │   │   ├─────────────┤
  │ Claude  │─────┼──▶│ Protocol│───┼──▶│   Slack     │
  ├─────────┤     │   │         │   │   ├─────────────┤
  │ Copilot │─────┘   │         │   └──▶│   Jira      │
  └─────────┘         └─────────┘       └─────────────┘

  Total: N + M = 3 + 3 = 6 implementations! ✅
```

---

## 📖 MCP Architecture

### The Three Components

```
┌──────────────────────────────────────────────────────────┐
│                    MCP ARCHITECTURE                        │
│                                                            │
│  ┌─────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │  MCP HOST   │    │  MCP CLIENT  │    │  MCP SERVER  │ │
│  │             │    │              │    │              │ │
│  │  The AI app │    │  Protocol    │    │  Wraps an    │ │
│  │  (VS Code,  │───▶│  connector   │───▶│  external    │ │
│  │   Claude    │    │  (built into │    │  service     │ │
│  │   Desktop)  │    │   the host)  │    │  (GitHub,    │ │
│  │             │    │              │    │   DB, etc.)  │ │
│  └─────────────┘    └──────────────┘    └──────────────┘ │
│                                                            │
│  Example: VS Code (host) ──▶ MCP Client ──▶ GitHub Server │
│                                                            │
└──────────────────────────────────────────────────────────┘
```

### What MCP Servers Provide

An MCP server exposes three types of capabilities:

```
┌──────────────────────────────────────────────────┐
│           MCP SERVER CAPABILITIES                 │
│                                                   │
│  1. TOOLS (actions the AI can take)              │
│     ┌──────────────────────────────────┐         │
│     │ create_issue(title, body, repo)  │         │
│     │ search_code(query, language)     │         │
│     │ run_query(sql, database)         │         │
│     └──────────────────────────────────┘         │
│                                                   │
│  2. RESOURCES (data the AI can read)             │
│     ┌──────────────────────────────────┐         │
│     │ file://project/README.md         │         │
│     │ db://users/schema                │         │
│     │ api://weather/current            │         │
│     └──────────────────────────────────┘         │
│                                                   │
│  3. PROMPTS (reusable prompt templates)          │
│     ┌──────────────────────────────────┐         │
│     │ code_review(code, language)      │         │
│     │ summarize_pr(pr_number)          │         │
│     │ explain_error(error_message)     │         │
│     └──────────────────────────────────┘         │
│                                                   │
└──────────────────────────────────────────────────┘
```

### Communication Protocol

MCP uses **JSON-RPC 2.0** over two transport types:

```
1. STDIO Transport (local processes):
   Host ──stdin/stdout──▶ Server Process
   
   Used for: local file access, database queries, CLI tools

2. SSE Transport (remote servers):
   Host ──HTTP/SSE──▶ Remote Server
   
   Used for: cloud services, shared team tools, SaaS integrations
```

---

## 🔧 Skills: Packaged Domain Knowledge

While MCP standardizes **tool access**, **Skills** standardize **domain knowledge**.

### What Are Skills?

Skills are bundles of:
- **Instructions**: Domain-specific prompts and guidelines
- **Tool configurations**: Which MCP tools to use and how
- **Patterns**: Reusable workflows for specific tasks

```
┌──────────────────────────────────────────────────┐
│                    SKILL                           │
│                                                    │
│  ┌────────────────────────────────────────────┐   │
│  │ SKILL.md                                    │   │
│  │                                             │   │
│  │ Name: "Database Migration Expert"           │   │
│  │                                             │   │
│  │ Instructions:                               │   │
│  │ - Always create reversible migrations       │   │
│  │ - Test migrations on a copy of prod data    │   │
│  │ - Include rollback scripts                  │   │
│  │ - Use Alembic for Python projects           │   │
│  │                                             │   │
│  │ Tools needed:                               │   │
│  │ - database MCP server                       │   │
│  │ - file system MCP server                    │   │
│  │                                             │   │
│  │ Example workflows:                          │   │
│  │ - "Create a new migration"                  │   │
│  │ - "Review pending migrations"               │   │
│  │ - "Rollback last migration"                 │   │
│  └────────────────────────────────────────────┘   │
│                                                    │
└──────────────────────────────────────────────────┘
```

### Skills + MCP = Plug-and-Play AI

```
Without Skills + MCP:
  Developer: "Help me create a database migration"
  AI: *generic advice that might not match your stack*

With Skills + MCP:
  Developer: "Help me create a database migration"
  AI: *uses migration skill instructions*
      *connects to your DB via MCP server*
      *reads current schema*
      *generates Alembic migration specific to YOUR project*
      *tests it against a copy*
```

---

## 📊 MCP Ecosystem (2025)

| MCP Server | What It Does | Example Tools |
|------------|-------------|---------------|
| GitHub | Repo management | create_issue, search_code, create_pr |
| PostgreSQL | Database access | run_query, get_schema, list_tables |
| Filesystem | File operations | read_file, write_file, search_files |
| Slack | Team communication | send_message, search_messages |
| Puppeteer | Web browsing | navigate, screenshot, click |
| Docker | Container management | run_container, list_containers |

---

## 💻 Hands-On Examples

### Example 1: Building an MCP Server
See [examples/01_mcp_server.py](examples/01_mcp_server.py)

### Example 2: MCP Client Integration
See [examples/02_mcp_client_demo.py](examples/02_mcp_client_demo.py)

---

## 🧠 Key Takeaways

1. **MCP** solves the N×M integration problem with a standard protocol
2. MCP servers expose **tools** (actions), **resources** (data), and **prompts** (templates)
3. **Skills** package domain knowledge + tool configurations for specific tasks
4. Together, MCP + Skills enable **plug-and-play AI capabilities**
5. This is the infrastructure layer that makes modern agentic AI practical

---

## 📚 Further Reading
- [MCP Specification](https://modelcontextprotocol.io/) — Official spec
- [MCP Servers Directory](https://github.com/modelcontextprotocol/servers) — Available servers
- [Building MCP Servers](https://modelcontextprotocol.io/quickstart/server) — Quick start guide

---

**← Previous:** [08: Context Engineering](../08-context-engineering/README.md)  
**Next →** [10: Modern Agentic AI — Putting It All Together](../10-modern-agentic-ai/README.md)
