const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const {
    FaBrain, FaPencilAlt, FaDatabase, FaTools, FaSyncAlt,
    FaRobot, FaUsers, FaSlidersH, FaPlug, FaRocket,
    FaChevronRight, FaLightbulb, FaExclamationTriangle,
    FaCheckCircle, FaArrowRight, FaCogs, FaCode, FaBookOpen,
    FaPython, FaCloud
} = require("react-icons/fa");

// ===== Icon Helper =====
function renderIconSvg(IconComponent, color, size = 256) {
    return ReactDOMServer.renderToStaticMarkup(
        React.createElement(IconComponent, { color, size: String(size) })
    );
}
async function iconToBase64Png(IconComponent, color, size = 256) {
    const svg = renderIconSvg(IconComponent, color, size);
    const pngBuffer = await sharp(Buffer.from(svg)).png().toBuffer();
    return "image/png;base64," + pngBuffer.toString("base64");
}

function loadDiagramPng(filename) {
    const p = path.join(__dirname, "diagrams", filename);
    if (!fs.existsSync(p)) return null;
    const buf = fs.readFileSync(p);
    // Read PNG dimensions from IHDR chunk (bytes 16-23)
    const width = buf.readUInt32BE(16);
    const height = buf.readUInt32BE(24);
    return {
        data: "image/png;base64," + buf.toString("base64"),
        width, height,
        ratio: width / height,
    };
}

// ===== Color Palette: Deep Tech / AI Theme =====
const C = {
    navy: "0F172A",
    darkSlate: "1E293B",
    slate: "334155",
    muted: "94A3B8",
    light: "E2E8F0",
    offWhite: "F8FAFC",
    white: "FFFFFF",
    accent: "06B6D4",  // cyan-500
    accentDk: "0891B2",  // cyan-600
    green: "10B981",
    amber: "F59E0B",
    rose: "F43F5E",
    violet: "8B5CF6",
};

const FONT_HEAD = "Trebuchet MS";
const FONT_BODY = "Calibri";

// Helper: common shadow factory
const mkShadow = () => ({ type: "outer", blur: 6, offset: 2, angle: 135, color: "000000", opacity: 0.12 });

async function buildPresentation() {
    let pres = new pptxgen();
    pres.layout = "LAYOUT_16x9";
    pres.author = "AI Evolution Learn";
    pres.title = "The Evolution of AI: From LLMs to Modern Agentic AI";

    // Pre-render all icons
    const icons = {};
    const iconMap = {
        brain: [FaBrain, C.accent],
        pencil: [FaPencilAlt, C.amber],
        database: [FaDatabase, C.green],
        tools: [FaTools, C.rose],
        sync: [FaSyncAlt, C.violet],
        robot: [FaRobot, C.accent],
        users: [FaUsers, C.green],
        sliders: [FaSlidersH, C.amber],
        plug: [FaPlug, C.rose],
        rocket: [FaRocket, C.accent],
        chevron: [FaChevronRight, C.white],
        lightbulb: [FaLightbulb, C.amber],
        warning: [FaExclamationTriangle, C.rose],
        check: [FaCheckCircle, C.green],
        arrow: [FaArrowRight, C.accent],
        cogs: [FaCogs, C.muted],
        code: [FaCode, C.accent],
        book: [FaBookOpen, C.violet],
        python: [FaPython, C.accent],
        cloud: [FaCloud, C.accentDk],
    };
    for (const [key, [comp, color]] of Object.entries(iconMap)) {
        icons[key] = await iconToBase64Png(comp, "#" + color);
    }
    // White variants for dark backgrounds
    for (const key of ["brain", "rocket", "check", "code", "lightbulb", "arrow", "book"]) {
        icons[key + "W"] = await iconToBase64Png(iconMap[key][0], "#FFFFFF");
    }

    // ============================================================
    // SLIDE 1: Title Slide
    // ============================================================
    let s1 = pres.addSlide();
    s1.background = { color: C.navy };
    // Decorative top bar
    s1.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.06, fill: { color: C.accent } });
    // Icon
    s1.addImage({ data: icons.brainW, x: 4.5, y: 0.8, w: 1.0, h: 1.0 });
    // Title
    s1.addText("The Evolution of AI", {
        x: 0.5, y: 1.9, w: 9, h: 0.8, fontSize: 40, fontFace: FONT_HEAD,
        color: C.white, bold: true, align: "center", margin: 0,
    });
    s1.addText("From LLMs to Modern Agentic AI", {
        x: 0.5, y: 2.65, w: 9, h: 0.6, fontSize: 22, fontFace: FONT_BODY,
        color: C.accent, align: "center", margin: 0,
    });
    // Subtitle line
    s1.addShape(pres.shapes.LINE, { x: 3.5, y: 3.4, w: 3, h: 0, line: { color: C.slate, width: 1 } });
    s1.addText("A 10-Module Hands-On Journey", {
        x: 0.5, y: 3.6, w: 9, h: 0.5, fontSize: 16, fontFace: FONT_BODY,
        color: C.muted, align: "center", margin: 0,
    });
    // Bottom info
    s1.addText("Python + OpenAI / Azure OpenAI  |  Code Examples Included", {
        x: 0.5, y: 4.7, w: 9, h: 0.4, fontSize: 12, fontFace: FONT_BODY,
        color: C.slate, align: "center", margin: 0,
    });

    // ============================================================
    // SLIDE 2: Course Overview / Roadmap
    // ============================================================
    let s2 = pres.addSlide();
    s2.background = { color: C.offWhite };
    s2.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.06, fill: { color: C.accent } });
    s2.addText("Course Roadmap", {
        x: 0.6, y: 0.3, w: 9, h: 0.6, fontSize: 32, fontFace: FONT_HEAD,
        color: C.navy, bold: true, margin: 0,
    });

    const modules = [
        ["01", "Foundation LLMs", icons.brain],
        ["02", "Prompt Engineering", icons.pencil],
        ["03", "RAG Pattern", icons.database],
        ["04", "Function Calling", icons.tools],
        ["05", "ReAct Pattern", icons.sync],
        ["06", "Agentic AI", icons.robot],
        ["07", "Multi-Agent Systems", icons.users],
        ["08", "Context Engineering", icons.sliders],
        ["09", "MCP & Skills", icons.plug],
        ["10", "Modern Agentic AI", icons.rocket],
    ];

    // 2 rows x 5 cols grid
    const startX = 0.35, startY = 1.15, cardW = 1.75, cardH = 1.9, gapX = 0.15, gapY = 0.2;
    for (let i = 0; i < modules.length; i++) {
        const col = i % 5, row = Math.floor(i / 5);
        const x = startX + col * (cardW + gapX);
        const y = startY + row * (cardH + gapY);
        // Card bg
        s2.addShape(pres.shapes.RECTANGLE, {
            x, y, w: cardW, h: cardH, fill: { color: C.white }, shadow: mkShadow(),
        });
        // Left accent
        s2.addShape(pres.shapes.RECTANGLE, {
            x, y, w: 0.06, h: cardH, fill: { color: C.accent },
        });
        // Module number
        s2.addText(modules[i][0], {
            x: x + 0.15, y: y + 0.15, w: 1.4, h: 0.3, fontSize: 11, fontFace: FONT_BODY,
            color: C.accentDk, bold: true, margin: 0,
        });
        // Icon
        s2.addImage({ data: modules[i][2], x: x + (cardW - 0.45) / 2, y: y + 0.5, w: 0.45, h: 0.45 });
        // Name
        s2.addText(modules[i][1], {
            x: x + 0.1, y: y + 1.1, w: cardW - 0.2, h: 0.7, fontSize: 12, fontFace: FONT_BODY,
            color: C.darkSlate, bold: true, align: "center", valign: "top", margin: 0,
        });
    }
    // Bottom arrow
    s2.addText("Each module solves a real pain point — building from simple to advanced", {
        x: 0.5, y: 5.1, w: 9, h: 0.35, fontSize: 11, fontFace: FONT_BODY,
        color: C.muted, italic: true, align: "center", margin: 0,
    });

    // ============================================================
    // SLIDE 3: The Pain-Point Story Arc
    // ============================================================
    let s3 = pres.addSlide();
    s3.background = { color: C.navy };
    s3.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.06, fill: { color: C.accent } });
    s3.addText("The Story Arc: Pain Points Drive Innovation", {
        x: 0.6, y: 0.25, w: 9, h: 0.6, fontSize: 28, fontFace: FONT_HEAD,
        color: C.white, bold: true, margin: 0,
    });

    const pains = [
        ["LLMs give random outputs", "Prompt Engineering (02)", C.amber],
        ["LLMs hallucinate", "RAG Pattern (03)", C.green],
        ["LLMs can't act", "Function Calling (04)", C.rose],
        ["Tool use without reasoning is blind", "ReAct Pattern (05)", C.violet],
        ["Agents are reactive, not proactive", "Agentic AI (06)", C.accent],
        ["One agent can't do everything", "Multi-Agent (07)", C.amber],
        ["Context window chaos", "Context Eng. (08)", C.green],
        ["N*M integration problem", "MCP & Skills (09)", C.rose],
    ];

    const pY = 1.05;
    for (let i = 0; i < pains.length; i++) {
        const y = pY + i * 0.54;
        // Pain label
        s3.addShape(pres.shapes.RECTANGLE, { x: 0.6, y, w: 4.0, h: 0.42, fill: { color: C.darkSlate } });
        s3.addText(pains[i][0], {
            x: 0.7, y, w: 3.8, h: 0.42, fontSize: 11, fontFace: FONT_BODY,
            color: C.light, valign: "middle", margin: 0,
        });
        // Arrow
        s3.addImage({ data: icons.arrow, x: 4.75, y: y + 0.06, w: 0.3, h: 0.3 });
        // Solution
        s3.addShape(pres.shapes.RECTANGLE, { x: 5.3, y, w: 4.1, h: 0.42, fill: { color: pains[i][2], transparency: 85 } });
        s3.addShape(pres.shapes.RECTANGLE, { x: 5.3, y, w: 0.06, h: 0.42, fill: { color: pains[i][2] } });
        s3.addText(pains[i][1], {
            x: 5.5, y, w: 3.8, h: 0.42, fontSize: 11, fontFace: FONT_BODY,
            color: C.white, bold: true, valign: "middle", margin: 0,
        });
    }

    // ============================================================
    // SLIDES 4–13: One slide per module
    // ============================================================
    const moduleSlides = [
        {
            num: "01", title: "Foundation LLMs", icon: "brain",
            subtitle: "Understanding the base technology",
            pain: "LLMs are stateless text completion engines with fundamental limits.",
            keyPoints: [
                "Transformer architecture: Attention Is All You Need (Vaswani, 2017)",
                "Emergent abilities at scale: few-shot learning, chain-of-thought, code gen",
                "Core limits: no memory, knowledge cutoff, hallucination, no actions",
                "Every API call is independent — the model forgets everything",
            ],
            example: "01_basic_llm_call.py — Simple OpenAI / Azure OpenAI API call",
            diagram: "module01_stateless.png",
            bgColor: C.offWhite,
        },
        {
            num: "02", title: "Prompt Engineering", icon: "pencil",
            subtitle: "Making LLMs actually useful",
            pain: "Raw prompts give inconsistent, low-quality outputs.",
            keyPoints: [
                "Zero-shot → Few-shot → Chain-of-Thought → System Prompts",
                "Structured output (JSON mode) for data pipelines",
                "Role patterns, self-consistency, Tree-of-Thought",
                "Necessary but insufficient — can't fix hallucination or knowledge cutoff",
            ],
            example: "01_prompting_techniques.py — Compare 4 techniques on one task",
            bgColor: C.offWhite,
        },
        {
            num: "03", title: "RAG Pattern", icon: "database",
            subtitle: "Retrieval-Augmented Generation",
            pain: "LLMs are frozen in time and hallucinate about private data.",
            keyPoints: [
                "Embed → Store → Retrieve → Augment → Generate",
                "Vector embeddings: semantic similarity via cosine distance",
                "Grounding eliminates hallucination for known knowledge",
                "Read-only pattern — can't take actions or iterate",
            ],
            example: "01_simple_rag.py — Full RAG pipeline from scratch with NumPy",
            diagram: "module03_rag.png",
            bgColor: C.offWhite,
        },
        {
            num: "04", title: "Function Calling & Tools", icon: "tools",
            subtitle: "LLMs that can act in the real world",
            pain: "LLMs can think but can't DO anything.",
            keyPoints: [
                "LLM decides WHAT to call; your code EXECUTES it (safety boundary)",
                "Tools defined via JSON Schema — LLM reads the schema",
                "OpenAI introduced function calling (June 2023)",
                "Single-turn only — no multi-step reasoning yet",
            ],
            example: "02_multi_tool_assistant.py — Project management assistant",
            diagram: "module04_tools.png",
            bgColor: C.offWhite,
        },
        {
            num: "05", title: "ReAct Pattern", icon: "sync",
            subtitle: "Reasoning + Acting — the foundation of agents",
            pain: "Function calling without reasoning is blind execution.",
            keyPoints: [
                "Thought → Action → Observation loop (Yao et al., 2022)",
                "Multi-step problem solving with adaptive planning",
                "Error recovery: retry, fallback, reason about failures",
                "Foundation of EVERY modern AI agent",
            ],
            example: "02_react_error_recovery.py — Agent that handles API failures",
            diagram: "module05_react.png",
            bgColor: C.offWhite,
        },
        {
            num: "06", title: "Agentic AI", icon: "robot",
            subtitle: "From chatbot to autonomous agent",
            pain: "ReAct agents are reactive, not proactive.",
            keyPoints: [
                "5 properties: Planning, Tool Use, Memory, Reflection, Autonomy",
                "Agent loop: Plan → Execute → Observe → Reflect → Adapt",
                "Short-term + long-term memory across sessions",
                "This is where Copilot, Cursor, Devin operate",
            ],
            example: "02_agent_with_memory.py — Agent with memory & self-reflection",
            bgColor: C.offWhite,
        },
        {
            num: "07", title: "Multi-Agent Systems", icon: "users",
            subtitle: "Specialization & collaboration",
            pain: "One agent can't handle complex multi-domain tasks.",
            keyPoints: [
                "Orchestrator: Manager delegates to specialist agents",
                "Pipeline: Sequential handoff (plan → code → review)",
                "Debate: Adversarial collaboration for quality",
                "Swarm: Dynamic routing to the right expert",
            ],
            example: "02_code_review_pipeline.py — Security + Performance reviewers",
            diagram: "module07_pipeline.png",
            bgColor: C.offWhite,
        },
        {
            num: "08", title: "Context Engineering", icon: "sliders",
            subtitle: "The #1 skill for production AI",
            pain: "Prompt engineering isn't enough for complex agent systems.",
            keyPoints: [
                "Curate the ENTIRE context window, not just the prompt",
                "Summarize old history, keep recent turns detailed",
                "Priority-based: P1 system+query, P2 code+docs, P3 prefs, P4 drop",
                "Dynamic selection: different queries need different context",
            ],
            example: "02_dynamic_context.py — Context pipeline selecting per-query",
            diagram: "module08_context.png",
            bgColor: C.offWhite,
        },
        {
            num: "09", title: "MCP & Skills", icon: "plug",
            subtitle: "Standardizing AI integration",
            pain: "N×M integration problem — every AI app needs custom integrations.",
            keyPoints: [
                "MCP = Standard protocol: any AI host ↔ any service ('USB for AI')",
                "Servers expose: Tools (actions), Resources (data), Prompts (templates)",
                "Skills = packaged domain knowledge + tool configurations",
                "N+M solution instead of N×M — write once, use everywhere",
            ],
            example: "02_mcp_client_demo.py — Multi-server MCP + LLM integration",
            diagram: "module09_mcp.png",
            bgColor: C.offWhite,
        },
        {
            num: "10", title: "Modern Agentic AI", icon: "rocket",
            subtitle: "Putting it all together",
            pain: "How do all these concepts combine in the real world?",
            keyPoints: [
                "GitHub Copilot, Claude Code, Cursor, Devin — all use these patterns",
                "LLM core + ReAct loop + tools via MCP + context engineering",
                "Planning agent with memory, reflection, and multi-agent collaboration",
                "Capstone: mini coding assistant combining Modules 01–09",
            ],
            example: "01_mini_agent.py — Complete agentic coding assistant",
            diagram: "module10_stack.png",
            bgColor: C.offWhite,
        },
    ];

    for (const mod of moduleSlides) {
        const s = pres.addSlide();
        s.background = { color: mod.bgColor };
        // Top accent bar
        s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.06, fill: { color: C.accent } });

        // Module number badge
        s.addShape(pres.shapes.RECTANGLE, {
            x: 0.5, y: 0.3, w: 0.65, h: 0.5, fill: { color: C.accent },
        });
        s.addText(mod.num, {
            x: 0.5, y: 0.3, w: 0.65, h: 0.5, fontSize: 18, fontFace: FONT_HEAD,
            color: C.white, bold: true, align: "center", valign: "middle", margin: 0,
        });

        // Title
        s.addText(mod.title, {
            x: 1.3, y: 0.28, w: 7.5, h: 0.55, fontSize: 28, fontFace: FONT_HEAD,
            color: C.navy, bold: true, margin: 0,
        });
        // Subtitle
        s.addText(mod.subtitle, {
            x: 1.3, y: 0.78, w: 7.5, h: 0.35, fontSize: 14, fontFace: FONT_BODY,
            color: C.muted, italic: true, margin: 0,
        });

        // Icon (right side)
        s.addImage({ data: icons[mod.icon], x: 8.8, y: 0.28, w: 0.65, h: 0.65 });

        // Divider
        s.addShape(pres.shapes.LINE, { x: 0.5, y: 1.2, w: 9, h: 0, line: { color: C.light, width: 1 } });

        // Pain point box (full width)
        s.addShape(pres.shapes.RECTANGLE, {
            x: 0.5, y: 1.4, w: 9, h: 0.55, fill: { color: "FEF2F2" },
        });
        s.addShape(pres.shapes.RECTANGLE, {
            x: 0.5, y: 1.4, w: 0.06, h: 0.55, fill: { color: C.rose },
        });
        s.addImage({ data: icons.warning, x: 0.7, y: 1.48, w: 0.35, h: 0.35 });
        s.addText(mod.pain, {
            x: 1.15, y: 1.4, w: 8.2, h: 0.55, fontSize: 13, fontFace: FONT_BODY,
            color: C.darkSlate, valign: "middle", margin: 0,
        });

        const diag = mod.diagram ? loadDiagramPng(mod.diagram) : null;

        if (diag) {
            // ---- SPLIT LAYOUT: bullets left, diagram right ----
            s.addText("Key Concepts", {
                x: 0.5, y: 2.15, w: 4.4, h: 0.38, fontSize: 15, fontFace: FONT_HEAD,
                color: C.navy, bold: true, margin: 0,
            });
            const bulletItems = mod.keyPoints.map((pt, idx) => ({
                text: pt,
                options: {
                    fontSize: 12, fontFace: FONT_BODY, color: C.darkSlate,
                    bullet: { code: "25CF", color: C.accent },
                    breakLine: idx < mod.keyPoints.length - 1,
                    paraSpaceAfter: 8,
                },
            }));
            s.addText(bulletItems, {
                x: 0.5, y: 2.55, w: 4.45, h: 2.2, margin: 0, valign: "top",
            });
            // Diagram card (right side) — use contain to preserve aspect ratio
            const cardX = 5.1, cardY = 2.1, cardW = 4.55, cardH = 2.7;
            const padW = 0.1, padH = 0.12;
            s.addShape(pres.shapes.RECTANGLE, {
                x: cardX, y: cardY, w: cardW, h: cardH, fill: { color: C.white }, shadow: mkShadow(),
            });
            s.addShape(pres.shapes.RECTANGLE, {
                x: cardX, y: cardY, w: cardW, h: 0.05, fill: { color: C.accent },
            });
            s.addImage({
                data: diag.data, x: cardX + padW, y: cardY + padH,
                w: cardW - padW * 2, h: cardH - padH * 2,
                sizing: { type: "contain", w: cardW - padW * 2, h: cardH - padH * 2 },
            });
        } else {
            // ---- FULL-WIDTH LAYOUT (no diagram) ----
            s.addText("Key Concepts", {
                x: 0.5, y: 2.15, w: 3, h: 0.4, fontSize: 16, fontFace: FONT_HEAD,
                color: C.navy, bold: true, margin: 0,
            });
            const bulletItems = mod.keyPoints.map((pt, idx) => ({
                text: pt,
                options: {
                    fontSize: 13, fontFace: FONT_BODY, color: C.darkSlate,
                    bullet: { code: "25CF", color: C.accent },
                    breakLine: idx < mod.keyPoints.length - 1,
                    paraSpaceAfter: 6,
                },
            }));
            s.addText(bulletItems, {
                x: 0.5, y: 2.55, w: 9, h: 2.2, margin: 0, valign: "top",
            });
        }

        // Example box (always full width at bottom)
        s.addShape(pres.shapes.RECTANGLE, {
            x: 0.5, y: 4.85, w: 9, h: 0.55, fill: { color: "F0FDF4" },
        });
        s.addShape(pres.shapes.RECTANGLE, {
            x: 0.5, y: 4.85, w: 0.06, h: 0.55, fill: { color: C.green },
        });
        s.addImage({ data: icons.code, x: 0.7, y: 4.93, w: 0.35, h: 0.35 });
        s.addText(mod.example, {
            x: 1.15, y: 4.85, w: 8.2, h: 0.55, fontSize: 12, fontFace: FONT_BODY,
            color: C.darkSlate, valign: "middle", margin: 0, italic: true,
        });
    }

    // ============================================================
    // SLIDE 14: Tech Stack / Setup
    // ============================================================
    let s14 = pres.addSlide();
    s14.background = { color: C.offWhite };
    s14.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.06, fill: { color: C.accent } });
    s14.addText("Getting Started", {
        x: 0.6, y: 0.3, w: 9, h: 0.6, fontSize: 30, fontFace: FONT_HEAD,
        color: C.navy, bold: true, margin: 0,
    });

    // Two columns
    // Left: Prerequisites
    s14.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 1.1, w: 4.3, h: 3.8, fill: { color: C.white }, shadow: mkShadow() });
    s14.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 1.1, w: 0.06, h: 3.8, fill: { color: C.accent } });
    s14.addImage({ data: icons.python, x: 0.7, y: 1.25, w: 0.4, h: 0.4 });
    s14.addText("Tech Stack & Setup", {
        x: 1.2, y: 1.25, w: 3.4, h: 0.4, fontSize: 18, fontFace: FONT_HEAD,
        color: C.navy, bold: true, margin: 0,
    });
    const setupItems = [
        { text: "Python 3.11+", options: { bullet: true, breakLine: true, fontSize: 13, fontFace: FONT_BODY, color: C.darkSlate, paraSpaceAfter: 4 } },
        { text: "OpenAI SDK (openai >= 1.12)", options: { bullet: true, breakLine: true, fontSize: 13, fontFace: FONT_BODY, color: C.darkSlate, paraSpaceAfter: 4 } },
        { text: "NumPy (for RAG embeddings)", options: { bullet: true, breakLine: true, fontSize: 13, fontFace: FONT_BODY, color: C.darkSlate, paraSpaceAfter: 4 } },
        { text: "pip install -r requirements.txt", options: { bullet: true, breakLine: true, fontSize: 13, fontFace: FONT_BODY, color: C.darkSlate, paraSpaceAfter: 4 } },
        { text: "Export OPENAI_API_KEY", options: { bullet: true, fontSize: 13, fontFace: FONT_BODY, color: C.darkSlate } },
    ];
    s14.addText(setupItems, { x: 0.75, y: 1.8, w: 3.8, h: 2.8, margin: 0 });

    // Right: Azure OpenAI option
    s14.addShape(pres.shapes.RECTANGLE, { x: 5.2, y: 1.1, w: 4.3, h: 3.8, fill: { color: C.white }, shadow: mkShadow() });
    s14.addShape(pres.shapes.RECTANGLE, { x: 5.2, y: 1.1, w: 0.06, h: 3.8, fill: { color: C.accentDk } });
    s14.addImage({ data: icons.cloud, x: 5.4, y: 1.25, w: 0.4, h: 0.4 });
    s14.addText("Azure OpenAI Option", {
        x: 5.9, y: 1.25, w: 3.4, h: 0.4, fontSize: 18, fontFace: FONT_HEAD,
        color: C.navy, bold: true, margin: 0,
    });
    const azureItems = [
        { text: "Set USE_AZURE_OPENAI=true", options: { bullet: true, breakLine: true, fontSize: 13, fontFace: FONT_BODY, color: C.darkSlate, paraSpaceAfter: 4 } },
        { text: "Set AZURE_OPENAI_API_KEY", options: { bullet: true, breakLine: true, fontSize: 13, fontFace: FONT_BODY, color: C.darkSlate, paraSpaceAfter: 4 } },
        { text: "Set AZURE_OPENAI_ENDPOINT", options: { bullet: true, breakLine: true, fontSize: 13, fontFace: FONT_BODY, color: C.darkSlate, paraSpaceAfter: 4 } },
        { text: "Set deployment name for model", options: { bullet: true, breakLine: true, fontSize: 13, fontFace: FONT_BODY, color: C.darkSlate, paraSpaceAfter: 4 } },
        { text: "Same code works for both!", options: { bullet: true, fontSize: 13, fontFace: FONT_BODY, color: C.accentDk, bold: true } },
    ];
    s14.addText(azureItems, { x: 5.45, y: 1.8, w: 3.8, h: 2.8, margin: 0 });

    // Bottom note
    s14.addText("All 21 examples support both OpenAI and Azure OpenAI — just switch env vars", {
        x: 0.5, y: 5.1, w: 9, h: 0.35, fontSize: 11, fontFace: FONT_BODY,
        color: C.muted, italic: true, align: "center", margin: 0,
    });

    // ============================================================
    // SLIDE 15: Key Takeaways
    // ============================================================
    let s15 = pres.addSlide();
    s15.background = { color: C.navy };
    s15.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.06, fill: { color: C.accent } });
    s15.addImage({ data: icons.lightbulbW, x: 0.6, y: 0.3, w: 0.5, h: 0.5 });
    s15.addText("Key Takeaways", {
        x: 1.2, y: 0.3, w: 8, h: 0.6, fontSize: 30, fontFace: FONT_HEAD,
        color: C.white, bold: true, margin: 0,
    });

    const takeaways = [
        ["AI is a tool, not magic", "Understand the components to use them effectively"],
        ["Context engineering is #1", "The most important skill for building production AI"],
        ["Agents are loops, not calls", "The power comes from iterative reasoning"],
        ["MCP is the future", "Standard protocol for plug-and-play AI capabilities"],
        ["Start simple, add complexity", "Chatbot → Tools → ReAct → Full Agent"],
    ];

    for (let i = 0; i < takeaways.length; i++) {
        const y = 1.1 + i * 0.85;
        s15.addShape(pres.shapes.RECTANGLE, {
            x: 0.6, y, w: 8.8, h: 0.7, fill: { color: C.darkSlate },
        });
        s15.addShape(pres.shapes.RECTANGLE, {
            x: 0.6, y, w: 0.06, h: 0.7, fill: { color: C.accent },
        });
        s15.addImage({ data: icons.checkW, x: 0.8, y: y + 0.12, w: 0.4, h: 0.4 });
        s15.addText(takeaways[i][0], {
            x: 1.35, y, w: 3.5, h: 0.7, fontSize: 15, fontFace: FONT_HEAD,
            color: C.white, bold: true, valign: "middle", margin: 0,
        });
        s15.addText(takeaways[i][1], {
            x: 5.0, y, w: 4.2, h: 0.7, fontSize: 13, fontFace: FONT_BODY,
            color: C.muted, valign: "middle", margin: 0,
        });
    }

    // ============================================================
    // SLIDE 16: Thank You / Resources
    // ============================================================
    let s16 = pres.addSlide();
    s16.background = { color: C.navy };
    s16.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.06, fill: { color: C.accent } });
    s16.addImage({ data: icons.rocketW, x: 4.5, y: 0.6, w: 1.0, h: 1.0 });
    s16.addText("Start Building!", {
        x: 0.5, y: 1.7, w: 9, h: 0.7, fontSize: 36, fontFace: FONT_HEAD,
        color: C.white, bold: true, align: "center", margin: 0,
    });
    s16.addText("The future is agentic — and it's built on these foundations", {
        x: 0.5, y: 2.4, w: 9, h: 0.5, fontSize: 16, fontFace: FONT_BODY,
        color: C.accent, align: "center", margin: 0,
    });

    s16.addShape(pres.shapes.LINE, { x: 3.5, y: 3.1, w: 3, h: 0, line: { color: C.slate, width: 1 } });

    const resources = [
        "ReAct Paper: arxiv.org/abs/2210.03629",
        "MCP Spec: modelcontextprotocol.io",
        "Anthropic Agent Guide: anthropic.com/research/building-effective-agents",
        "OpenAI Agents SDK: github.com/openai/openai-agents-python",
    ];
    const resItems = resources.map((r, i) => ({
        text: r,
        options: {
            fontSize: 12, fontFace: FONT_BODY, color: C.muted,
            bullet: { code: "25CF", color: C.accent },
            breakLine: i < resources.length - 1, paraSpaceAfter: 4,
        },
    }));
    s16.addText(resItems, { x: 2.0, y: 3.3, w: 6, h: 1.8, margin: 0 });

    s16.addText("Thank You!", {
        x: 0.5, y: 5.0, w: 9, h: 0.45, fontSize: 14, fontFace: FONT_BODY,
        color: C.slate, align: "center", margin: 0,
    });

    // ===== WRITE FILE =====
    await pres.writeFile({ fileName: "/home/alpha/git-clone/ai-evolution-learn/AI_Evolution_Presentation.pptx" });
    console.log("Presentation saved to AI_Evolution_Presentation.pptx");
}

buildPresentation().catch(console.error);
