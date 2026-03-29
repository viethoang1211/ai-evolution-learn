// Generate SVG diagrams for flows that Mermaid can't render at landscape ratios
const sharp = require("sharp");
const fs = require("fs");
const path = require("path");

const C = {
    cyan: "#06B6D4", violet: "#8B5CF6", green: "#10B981",
    amber: "#F59E0B", rose: "#F43F5E", navy: "#0F172A",
    slate: "#64748B", light: "#E2E8F0",
    bgCyan: "#E0F2FE", bgViolet: "#EEF2FF", bgGreen: "#ECFDF5",
    bgAmber: "#FFF7ED", bgRose: "#FEF2F2", bgBlue: "#F0F9FF",
};

function box(x, y, w, h, fill, stroke, text, textColor = C.navy, fontSize = 13) {
    const lines = text.split("\n");
    const lineH = fontSize + 4;
    const textStartY = y + h / 2 - (lines.length * lineH) / 2 + fontSize;
    const textSvg = lines.map((l, i) =>
        `<text x="${x + w / 2}" y="${textStartY + i * lineH}" text-anchor="middle" fill="${textColor}" font-family="Arial,sans-serif" font-size="${fontSize}" font-weight="${i === 0 ? 'bold' : 'normal'}">${esc(l)}</text>`
    ).join("\n");
    return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="6" fill="${fill}" stroke="${stroke}" stroke-width="2"/>\n${textSvg}`;
}

function pill(x, y, w, h, fill, stroke, text, textColor = C.navy, fontSize = 13) {
    const r = h / 2;
    return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r}" fill="${fill}" stroke="${stroke}" stroke-width="2"/>
<text x="${x + w / 2}" y="${y + h / 2 + fontSize / 3}" text-anchor="middle" fill="${textColor}" font-family="Arial,sans-serif" font-size="${fontSize}" font-weight="bold">${esc(text)}</text>`;
}

function diamond(cx, cy, w, h, fill, stroke, text, fontSize = 12) {
    const pts = `${cx},${cy - h / 2} ${cx + w / 2},${cy} ${cx},${cy + h / 2} ${cx - w / 2},${cy}`;
    return `<polygon points="${pts}" fill="${fill}" stroke="${stroke}" stroke-width="2"/>
<text x="${cx}" y="${cy + fontSize / 3}" text-anchor="middle" fill="${C.navy}" font-family="Arial,sans-serif" font-size="${fontSize}" font-weight="bold">${esc(text)}</text>`;
}

function arrow(x1, y1, x2, y2, label = "", curved = false) {
    const id = `a${Math.random().toString(36).slice(2, 8)}`;
    let pathD;
    if (curved) {
        const mx = (x1 + x2) / 2, my = (y1 + y2) / 2;
        const cx = x1 < x2 ? mx : x1 + 40;
        const cy = y1 < y2 ? my : y1 - 40;
        pathD = `M${x1},${y1} Q${cx},${cy} ${x2},${y2}`;
    } else {
        pathD = `M${x1},${y1} L${x2},${y2}`;
    }
    let svg = `<defs><marker id="${id}" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="${C.slate}"/></marker></defs>
<path d="${pathD}" stroke="${C.slate}" stroke-width="2" fill="none" marker-end="url(#${id})"/>`;
    if (label) {
        const lx = (x1 + x2) / 2, ly = (y1 + y2) / 2 - 8;
        svg += `\n<text x="${lx}" y="${ly}" text-anchor="middle" fill="${C.slate}" font-family="Arial,sans-serif" font-size="11" font-style="italic">${esc(label)}</text>`;
    }
    return svg;
}

function esc(s) { return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }

async function renderSvg(svgContent, w, h, filename) {
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">\n${svgContent}\n</svg>`;
    const buf = await sharp(Buffer.from(svg)).png().toBuffer();
    fs.writeFileSync(path.join(__dirname, filename), buf);
    console.log(`  ${filename}: ${w}x${h}  ratio=${(w / h).toFixed(2)}`);
}

async function main() {
    console.log("Generating custom SVG diagrams...");

    // ============================================================
    // Module 04 — Function Calling & Tools (target: ~750x440)
    // Layout: User + Tools → LLM → Code → API → LLM → Response
    //         Two inputs at top-left, flowing right then down-right
    // ============================================================
    const w4 = 750, h4 = 400;
    const m04 = [
        // Row 1: User Request + Tool Definitions
        pill(20, 30, 150, 44, C.bgCyan, C.cyan, "User Request"),
        box(20, 100, 150, 50, C.bgAmber, C.amber, "Tool Definitions\n(JSON Schema)"),
        arrow(170, 52, 230, 80),
        arrow(170, 125, 230, 100),

        // Row 1→2: LLM selects
        box(230, 60, 180, 60, C.bgViolet, C.violet, "LLM\nselects tool + args"),
        arrow(410, 90, 460, 90, "tool_call"),

        // Row 2: Your Code
        box(460, 60, 150, 60, C.bgGreen, C.green, "Your Code\nexecutes safely"),
        arrow(535, 120, 535, 160),

        // Row 3: External API
        box(460, 160, 150, 50, C.bgCyan, C.cyan, "External API / DB"),
        arrow(460, 185, 400, 185, "result"),

        // Row 3: LLM formats
        box(220, 160, 180, 55, C.bgViolet, C.violet, "LLM\nformats response"),
        arrow(310, 215, 310, 260),

        // Row 4: Answer
        pill(230, 260, 160, 44, C.bgGreen, C.green, "Natural Response"),

        // Labels
        `<rect x="${490}" y="${280}" width="220" height="90" rx="8" fill="#F8FAFC" stroke="${C.light}" stroke-width="1.5" stroke-dasharray="6,3"/>`,
        `<text x="600" y="310" text-anchor="middle" fill="${C.slate}" font-family="Arial,sans-serif" font-size="11" font-weight="bold">Safety Boundary</text>`,
        `<text x="600" y="328" text-anchor="middle" fill="${C.slate}" font-family="Arial,sans-serif" font-size="10">LLM DECIDES what to call</text>`,
        `<text x="600" y="346" text-anchor="middle" fill="${C.slate}" font-family="Arial,sans-serif" font-size="10">Your code EXECUTES it</text>`,
    ].join("\n");
    await renderSvg(m04, w4, h4, "module04_tools.png");

    // ============================================================
    // Module 05 — ReAct Pattern (target: ~750x420)
    // Layout: Query → [Loop: Thought → Action → Observation] → Answer
    // ============================================================
    const w5 = 750, h5 = 400;
    // Loop background box
    const loopX = 160, loopY = 20, loopW = 410, loopH = 250;
    const m05 = [
        // Query pill
        pill(20, 120, 120, 44, C.bgCyan, C.cyan, "User Query"),
        arrow(140, 142, 190, 72),

        // Loop box
        `<rect x="${loopX}" y="${loopY}" width="${loopW}" height="${loopH}" rx="10" fill="#F8FAFC" stroke="${C.cyan}" stroke-width="2" stroke-dasharray="8,4"/>`,
        `<text x="${loopX + loopW / 2}" y="${loopY + 18}" text-anchor="middle" fill="${C.cyan}" font-family="Arial,sans-serif" font-size="12" font-weight="bold">ReAct Loop</text>`,

        // Thought
        box(190, 40, 140, 55, C.bgViolet, C.violet, "THOUGHT\nAnalyze problem"),
        arrow(330, 67, 370, 67),

        // Action  
        box(370, 40, 140, 55, C.bgGreen, C.green, "ACTION\nCall tool + args"),
        arrow(440, 95, 440, 130),

        // Observation
        box(300, 130, 160, 55, C.bgAmber, C.amber, "OBSERVATION\nRead tool result"),
        arrow(300, 157, 260, 95, "", true),  // Back to Thought

        // Back-loop label
        `<text x="248" y="130" text-anchor="middle" fill="${C.slate}" font-family="Arial,sans-serif" font-size="10" font-style="italic">loop</text>`,

        // Decision diamond
        arrow(460, 157, 530, 157),
        diamond(580, 160, 90, 70, C.bgBlue, C.cyan, "Goal?"),

        // No arrow (back to loop)
        `<path d="M580,195 Q580,250 400,250 Q190,250 190,95" stroke="${C.slate}" stroke-width="1.5" fill="none" stroke-dasharray="5,3"/>`,
        `<text x="400" y="268" text-anchor="middle" fill="${C.rose}" font-family="Arial,sans-serif" font-size="11" font-weight="bold">No — need more info</text>`,

        // Yes → Answer
        arrow(625, 160, 680, 160),
        pill(680, 138, 55, 44, C.bgGreen, C.green, "Yes"),
        `<text x="708" y="200" text-anchor="middle" fill="${C.green}" font-family="Arial,sans-serif" font-size="11" font-weight="bold">Final Answer</text>`,
    ].join("\n");
    await renderSvg(m05, w5, h5, "module05_react.png");

    // ============================================================
    // Module 07 — Multi-Agent Pipeline (target: ~750x380)
    // Layout: Task → Orchestrator → Architect → Coder ⇄ Reviewer → Done
    //         Organized as 2 rows with clear phase labels
    // ============================================================
    const w7 = 750, h7 = 370;
    const m07 = [
        // Phase labels (background boxes)
        `<rect x="10" y="10" width="240" height="160" rx="10" fill="#EFF6FF" stroke="#3B82F6" stroke-width="1.5"/>`,
        `<text x="130" y="30" text-anchor="middle" fill="#3B82F6" font-family="Arial,sans-serif" font-size="12" font-weight="bold">Planning</text>`,

        `<rect x="260" y="10" width="230" height="160" rx="10" fill="#F0FDF4" stroke="#10B981" stroke-width="1.5"/>`,
        `<text x="375" y="30" text-anchor="middle" fill="#10B981" font-family="Arial,sans-serif" font-size="12" font-weight="bold">Design &amp; Build</text>`,

        `<rect x="500" y="10" width="240" height="160" rx="10" fill="#FFF7ED" stroke="#F59E0B" stroke-width="1.5"/>`,
        `<text x="620" y="30" text-anchor="middle" fill="#F59E0B" font-family="Arial,sans-serif" font-size="12" font-weight="bold">Quality Gate</text>`,

        // Task
        pill(40, 50, 180, 40, C.bgCyan, C.cyan, "Complex Task"),
        arrow(130, 90, 130, 105),

        // Orchestrator
        box(40, 105, 180, 50, C.bgCyan, C.cyan, "Orchestrator\nBreaks down task"),
        arrow(220, 130, 280, 130),

        // Architect
        box(280, 50, 190, 50, C.bgGreen, C.green, "Architect\nDesigns solution"),
        arrow(375, 100, 375, 115),

        // Coder
        box(280, 115, 190, 50, C.bgViolet, C.violet, "Coder\nImplements from spec"),
        arrow(470, 140, 520, 100),

        // Reviewer
        box(520, 50, 200, 55, C.bgAmber, C.amber, "Reviewer\nSecurity + Performance"),
        arrow(620, 105, 620, 130),

        // Revision loop
        `<path d="M520,77 Q490,77 490,140 Q490,140 470,140" stroke="${C.rose}" stroke-width="2" fill="none"/>`,
        `<polygon points="470,136 470,144 462,140" fill="${C.rose}"/>`,
        `<text x="478" y="108" text-anchor="middle" fill="${C.rose}" font-family="Arial,sans-serif" font-size="10" font-weight="bold">Revision</text>`,

        // Approved → Done
        pill(560, 130, 120, 36, C.bgGreen, C.green, "Done"),
        `<text x="620" y="180" text-anchor="middle" fill="${C.green}" font-family="Arial,sans-serif" font-size="10" font-weight="bold">Approved</text>`,

        // Summary box at bottom
        `<rect x="60" y="210" width="630" height="140" rx="10" fill="#F8FAFC" stroke="${C.light}" stroke-width="1.5"/>`,
        `<text x="375" y="236" text-anchor="middle" fill="${C.navy}" font-family="Arial,sans-serif" font-size="13" font-weight="bold">Each agent is a specialist with a focused system prompt</text>`,
        `<text x="375" y="264" text-anchor="middle" fill="${C.slate}" font-family="Arial,sans-serif" font-size="11">Orchestrator plans | Architect designs | Coder builds | Reviewer validates</text>`,
        `<text x="375" y="290" text-anchor="middle" fill="${C.slate}" font-family="Arial,sans-serif" font-size="11">Reviewer can REJECT and send code back, creating a feedback loop</text>`,
        `<text x="375" y="318" text-anchor="middle" fill="${C.violet}" font-family="Arial,sans-serif" font-size="11" font-weight="bold">Specialization beats generalization for complex tasks</text>`,
    ].join("\n");
    await renderSvg(m07, w7, h7, "module07_pipeline.png");

    console.log("Done!");
}

main().catch(console.error);
