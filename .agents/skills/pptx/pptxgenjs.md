# PptxGenJS Tutorial

## Setup & Basic Structure

```javascript
const pptxgen = require("pptxgenjs");

let pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';  // or 'LAYOUT_16x10', 'LAYOUT_4x3', 'LAYOUT_WIDE'
pres.author = 'Your Name';
pres.title = 'Presentation Title';

let slide = pres.addSlide();
slide.addText("Hello World!", { x: 0.5, y: 0.5, fontSize: 36, color: "363636" });

pres.writeFile({ fileName: "Presentation.pptx" });
```

## Layout Dimensions

Slide dimensions (coordinates in inches):
- `LAYOUT_16x9`: 10" × 5.625" (default)
- `LAYOUT_16x10`: 10" × 6.25"
- `LAYOUT_4x3`: 10" × 7.5"
- `LAYOUT_WIDE`: 13.3" × 7.5"

---

## Text & Formatting

```javascript
// Basic text
slide.addText("Simple Text", {
  x: 1, y: 1, w: 8, h: 2, fontSize: 24, fontFace: "Arial",
  color: "363636", bold: true, align: "center", valign: "middle"
});

// Character spacing (use charSpacing, not letterSpacing which is silently ignored)
slide.addText("SPACED TEXT", { x: 1, y: 1, w: 8, h: 1, charSpacing: 6 });

// Rich text arrays
slide.addText([
  { text: "Bold ", options: { bold: true } },
  { text: "Italic ", options: { italic: true } }
], { x: 1, y: 3, w: 8, h: 1 });

// Multi-line text (requires breakLine: true)
slide.addText([
  { text: "Line 1", options: { breakLine: true } },
  { text: "Line 2", options: { breakLine: true } },
  { text: "Line 3" }  // Last item doesn't need breakLine
], { x: 0.5, y: 0.5, w: 8, h: 2 });

// Text box margin (internal padding)
slide.addText("Title", {
  x: 0.5, y: 0.3, w: 9, h: 0.6,
  margin: 0  // Use 0 when aligning text with other elements like shapes or icons
});
```

**Tip:** Text boxes have internal margin by default. Set `margin: 0` when you need text to align precisely with shapes, lines, or icons at the same x-position.

---

## Lists & Bullets

```javascript
// ✅ CORRECT: Multiple bullets
slide.addText([
  { text: "First item", options: { bullet: true, breakLine: true } },
  { text: "Second item", options: { bullet: true, breakLine: true } },
  { text: "Third item", options: { bullet: true } }
], { x: 0.5, y: 0.5, w: 8, h: 3 });

// ❌ WRONG: Never use unicode bullets
slide.addText("• First item", { ... });  // Creates double bullets

// Sub-items and numbered lists
{ text: "Sub-item", options: { bullet: true, indentLevel: 1 } }
{ text: "First", options: { bullet: { type: "number" }, breakLine: true } }
```

---

## Shapes

```javascript
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 0.8, w: 1.5, h: 3.0,
  fill: { color: "FF0000" }, line: { color: "000000", width: 2 }
});

slide.addShape(pres.shapes.OVAL, { x: 4, y: 1, w: 2, h: 2, fill: { color: "0000FF" } });

slide.addShape(pres.shapes.LINE, {
  x: 1, y: 3, w: 5, h: 0, line: { color: "FF0000", width: 3, dashType: "dash" }
});

// With transparency
slide.addShape(pres.shapes.RECTANGLE, {
  x: 1, y: 1, w: 3, h: 2,
  fill: { color: "0088CC", transparency: 50 }
});

// Rounded rectangle (rectRadius only works with ROUNDED_RECTANGLE, not RECTANGLE)
// ⚠️ Don't pair with rectangular accent overlays — they won't cover rounded corners. Use RECTANGLE instead.
slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 1, y: 1, w: 3, h: 2,
  fill: { color: "FFFFFF" }, rectRadius: 0.1
});

// With shadow
slide.addShape(pres.shapes.RECTANGLE, {
  x: 1, y: 1, w: 3, h: 2,
  fill: { color: "FFFFFF" },
  shadow: { type: "outer", color: "000000", blur: 6, offset: 2, angle: 135, opacity: 0.15 }
});
```

Shadow options:

| Property | Type | Range | Notes |
|----------|------|-------|-------|
| `type` | string | `"outer"`, `"inner"` | |
| `color` | string | 6-char hex (e.g. `"000000"`) | No `#` prefix, no 8-char hex — see Common Pitfalls |
| `blur` | number | 0-100 pt | |
| `offset` | number | 0-200 pt | **Must be non-negative** — negative values corrupt the file |
| `angle` | number | 0-359 degrees | Direction the shadow falls (135 = bottom-right, 270 = upward) |
| `opacity` | number | 0.0-1.0 | Use this for transparency, never encode in color string |

To cast a shadow upward (e.g. on a footer bar), use `angle: 270` with a positive offset — do **not** use a negative offset.

**Note**: Gradient fills are not natively supported. Use a gradient image as a background instead.

---

## Images

### Image Sources

```javascript
// From file path
slide.addImage({ path: "images/chart.png", x: 1, y: 1, w: 5, h: 3 });

// From URL
slide.addImage({ path: "https://example.com/image.jpg", x: 1, y: 1, w: 5, h: 3 });

// From base64 (faster, no file I/O)
slide.addImage({ data: "image/png;base64,iVBORw0KGgo...", x: 1, y: 1, w: 5, h: 3 });
```

### Image Options

```javascript
slide.addImage({
  path: "image.png",
  x: 1, y: 1, w: 5, h: 3,
  rotate: 45,              // 0-359 degrees
  rounding: true,          // Circular crop
  transparency: 50,        // 0-100
  flipH: true,             // Horizontal flip
  flipV: false,            // Vertical flip
  altText: "Description",  // Accessibility
  hyperlink: { url: "https://example.com" }
});
```

### Image Sizing Modes

```javascript
// Contain - fit inside, preserve ratio
{ sizing: { type: 'contain', w: 4, h: 3 } }

// Cover - fill area, preserve ratio (may crop)
{ sizing: { type: 'cover', w: 4, h: 3 } }

// Crop - cut specific portion
{ sizing: { type: 'crop', x: 0.5, y: 0.5, w: 2, h: 2 } }
```

### Calculate Dimensions (preserve aspect ratio)

```javascript
const origWidth = 1978, origHeight = 923, maxHeight = 3.0;
const calcWidth = maxHeight * (origWidth / origHeight);
const centerX = (10 - calcWidth) / 2;

slide.addImage({ path: "image.png", x: centerX, y: 1.2, w: calcWidth, h: maxHeight });
```

### Supported Formats

- **Standard**: PNG, JPG, GIF (animated GIFs work in Microsoft 365)
- **SVG**: Works in modern PowerPoint/Microsoft 365

---

## Mermaid Diagrams

Render Mermaid diagrams to PNG and embed them in slides for visual architecture/flow explanations. Text-only slides are forgettable — diagrams make complex concepts instantly understandable.

### Setup

```bash
npm install -g @mermaid-js/mermaid-cli
```

### Workflow

1. **Create `.mmd` files** with Mermaid syntax
2. **Create a config** for consistent styling (colors matching your palette)
3. **Render to PNG** with `mmdc`
4. **Load and embed** in slides using `addImage`

### Mermaid Config (match your slide palette)

Create a `mermaid.config.json` that matches your presentation colors:

```json
{
  "theme": "base",
  "themeVariables": {
    "primaryColor": "#E0F2FE",
    "primaryTextColor": "#0F172A",
    "primaryBorderColor": "#06B6D4",
    "lineColor": "#64748B",
    "fontFamily": "Arial, sans-serif",
    "fontSize": "15px"
  }
}
```

### Rendering Diagrams

```bash
# Render with transparent background
mmdc -i diagram.mmd -o diagram.png -c mermaid.config.json -w 600 -H 520 -b transparent
```

- `-w` / `-H`: viewport size (the diagram auto-fits within this)
- `-b transparent`: clean background for embedding on any slide color

### Loading and Embedding in Slides

```javascript
const fs = require("fs");
const path = require("path");

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

const diag = loadDiagramPng("architecture.png");
slide.addImage({
    data: diag.data, x: 5.1, y: 2.1, w: 4.5, h: 2.6,
    sizing: { type: "contain", w: 4.5, h: 2.6 },  // Preserve aspect ratio!
});
```

### Aspect Ratio Rules

**CRITICAL: Never stretch diagrams.** Always use `sizing: { type: "contain" }` to preserve the original aspect ratio.

**All diagrams must have ratio (w/h) ≥ 0.7** to fit the split layout (bullets left, diagram card right). If a diagram renders too tall or too narrow, fix the diagram — don't add separate slides (they look terrible with tiny images on a landscape slide).

```javascript
const diag = loadDiagramPng(mod.diagram);
if (diag) {
    // Split layout: bullets left 4.5", diagram card right 4.5"
    slide.addImage({
        data: diag.data, x: 5.2, y: 2.2, w: 4.3, h: 2.5,
        sizing: { type: "contain", w: 4.3, h: 2.5 },
    });
} else {
    // No diagram — full-width text layout
}
```

### Fixing Bad Aspect Ratios

Mermaid often produces diagrams with aspect ratios that don't work for landscape slides:

| Mermaid direction | Typical problem |
|-------------------|-----------------|
| `flowchart TD` | Too tall/narrow (ratio 0.3-0.6) for sequential flows |
| `flowchart LR` | Too flat/wide (ratio 5-12:1) for multi-step flows |
| `TD` with `LR` subgraphs | Better but still often < 0.7 for complex graphs |

**Prevention strategies (in order of preference):**

1. **Restructure the Mermaid diagram** — use subgraphs, group parallel nodes, reduce nesting. Target viewport `-w 900 -H 440` for a ~2:1 ratio
2. **Use `flowchart LR` with short node text** — works for simple 3-5 step flows
3. **Custom SVG generator** — when Mermaid can't produce good ratios, hand-craft SVG and rasterize with `sharp` (see below)

### Custom SVG Fallback (for Mermaid-resistant diagrams)

When Mermaid can't produce a landscape-friendly layout (common with sequential pipelines, multi-phase flows, or decision trees), generate SVGs programmatically with pixel-level control:

```javascript
const sharp = require("sharp");
const fs = require("fs");

// Helper functions for SVG primitives
function esc(s) { return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }

function box(x, y, w, h, fill, stroke, text, textColor = "#0F172A", fontSize = 13) {
    return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="8"
            fill="${fill}" stroke="${stroke}" stroke-width="1.5"/>
            <text x="${x + w / 2}" y="${y + h / 2 + fontSize * 0.35}"
            text-anchor="middle" font-size="${fontSize}" fill="${textColor}"
            font-family="Arial, sans-serif">${esc(text)}</text>`;
}

function arrow(x1, y1, x2, y2, color = "#64748B") {
    return `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}"
            stroke="${color}" stroke-width="1.5" marker-end="url(#ah)"/>`;
}

// Build SVG with your exact target dimensions
const W = 750, H = 400;  // Target ~1.88:1 ratio
const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}">
  <defs><marker id="ah" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
    <path d="M0,0 L8,3 L0,6Z" fill="#64748B"/></marker></defs>
  ${box(20, 50, 140, 40, "#E0F2FE", "#06B6D4", "Step 1")}
  ${arrow(160, 70, 200, 70)}
  ${box(200, 50, 140, 40, "#E0F2FE", "#06B6D4", "Step 2")}
</svg>`;

await sharp(Buffer.from(svg)).png().toFile("diagrams/my_diagram.png");
```

**When to use custom SVGs:**
- Sequential pipelines with 4+ stages (Mermaid TD = too tall, LR = too wide)
- Complex decision flows where Mermaid auto-layout produces bad proportions
- Diagrams needing precise alignment or grid layouts
- Any diagram where Mermaid output has ratio < 0.7 after trying restructoring

**Key rules:**
- Set explicit SVG `width` and `height` to control the exact ratio (target 1.5:1 to 2.5:1)
- Escape `&` as `&amp;` and `<`/`>` in all text content (XML requirement)
- Avoid Unicode symbols in text — use plain words instead
- Use `sharp` for rasterization (handles SVG→PNG reliably)

### Diagram Card Styling

Wrap diagrams in a white card with a colored top accent for polish:

```javascript
const cardX = 5.1, cardY = 2.1, cardW = 4.55, cardH = 2.7;
// White card with shadow
slide.addShape(pres.shapes.RECTANGLE, {
    x: cardX, y: cardY, w: cardW, h: cardH,
    fill: { color: "FFFFFF" }, shadow: mkShadow(),
});
// Colored top border
slide.addShape(pres.shapes.RECTANGLE, {
    x: cardX, y: cardY, w: cardW, h: 0.05,
    fill: { color: "06B6D4" },
});
// Diagram with padding inside card
slide.addImage({
    data: diag.data,
    x: cardX + 0.1, y: cardY + 0.12,
    w: cardW - 0.2, h: cardH - 0.24,
    sizing: { type: "contain", w: cardW - 0.2, h: cardH - 0.24 },
});
```

### Mermaid Diagram Tips

- **Don't blindly default to `flowchart TD`** — it often produces tall/narrow diagrams (ratio < 0.7) for sequential flows. Test the actual rendered dimensions before committing
- **Try `flowchart LR`** for simple 3-5 step linear flows — shorter text keeps them compact
- **Use subgraphs** to group related concepts and reduce vertical/horizontal sprawl
- **Keep node text short** — long text creates wide nodes that don't scale well
- **Color nodes** with `style` to match your slide palette
- **Always verify dimensions** after rendering — run `identify diagram.png` or read the PNG IHDR header to check the actual ratio
- **If ratio < 0.7 after restructuring**, switch to the custom SVG approach instead of fighting Mermaid's auto-layout
- **Render with explicit viewport**: `mmdc -w 900 -H 440 -b transparent` to hint at the desired proportions

---

## Icons

Use react-icons to generate SVG icons, then rasterize to PNG for universal compatibility.

### Setup

```javascript
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const { FaCheckCircle, FaChartLine } = require("react-icons/fa");

function renderIconSvg(IconComponent, color = "#000000", size = 256) {
  return ReactDOMServer.renderToStaticMarkup(
    React.createElement(IconComponent, { color, size: String(size) })
  );
}

async function iconToBase64Png(IconComponent, color, size = 256) {
  const svg = renderIconSvg(IconComponent, color, size);
  const pngBuffer = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + pngBuffer.toString("base64");
}
```

### Add Icon to Slide

```javascript
const iconData = await iconToBase64Png(FaCheckCircle, "#4472C4", 256);

slide.addImage({
  data: iconData,
  x: 1, y: 1, w: 0.5, h: 0.5  // Size in inches
});
```

**Note**: Use size 256 or higher for crisp icons. The size parameter controls the rasterization resolution, not the display size on the slide (which is set by `w` and `h` in inches).

### Icon Libraries

Install: `npm install -g react-icons react react-dom sharp`

Popular icon sets in react-icons:
- `react-icons/fa` - Font Awesome
- `react-icons/md` - Material Design
- `react-icons/hi` - Heroicons
- `react-icons/bi` - Bootstrap Icons

---

## Slide Backgrounds

```javascript
// Solid color
slide.background = { color: "F1F1F1" };

// Color with transparency
slide.background = { color: "FF3399", transparency: 50 };

// Image from URL
slide.background = { path: "https://example.com/bg.jpg" };

// Image from base64
slide.background = { data: "image/png;base64,iVBORw0KGgo..." };
```

---

## Tables

```javascript
slide.addTable([
  ["Header 1", "Header 2"],
  ["Cell 1", "Cell 2"]
], {
  x: 1, y: 1, w: 8, h: 2,
  border: { pt: 1, color: "999999" }, fill: { color: "F1F1F1" }
});

// Advanced with merged cells
let tableData = [
  [{ text: "Header", options: { fill: { color: "6699CC" }, color: "FFFFFF", bold: true } }, "Cell"],
  [{ text: "Merged", options: { colspan: 2 } }]
];
slide.addTable(tableData, { x: 1, y: 3.5, w: 8, colW: [4, 4] });
```

---

## Charts

```javascript
// Bar chart
slide.addChart(pres.charts.BAR, [{
  name: "Sales", labels: ["Q1", "Q2", "Q3", "Q4"], values: [4500, 5500, 6200, 7100]
}], {
  x: 0.5, y: 0.6, w: 6, h: 3, barDir: 'col',
  showTitle: true, title: 'Quarterly Sales'
});

// Line chart
slide.addChart(pres.charts.LINE, [{
  name: "Temp", labels: ["Jan", "Feb", "Mar"], values: [32, 35, 42]
}], { x: 0.5, y: 4, w: 6, h: 3, lineSize: 3, lineSmooth: true });

// Pie chart
slide.addChart(pres.charts.PIE, [{
  name: "Share", labels: ["A", "B", "Other"], values: [35, 45, 20]
}], { x: 7, y: 1, w: 5, h: 4, showPercent: true });
```

### Better-Looking Charts

Default charts look dated. Apply these options for a modern, clean appearance:

```javascript
slide.addChart(pres.charts.BAR, chartData, {
  x: 0.5, y: 1, w: 9, h: 4, barDir: "col",

  // Custom colors (match your presentation palette)
  chartColors: ["0D9488", "14B8A6", "5EEAD4"],

  // Clean background
  chartArea: { fill: { color: "FFFFFF" }, roundedCorners: true },

  // Muted axis labels
  catAxisLabelColor: "64748B",
  valAxisLabelColor: "64748B",

  // Subtle grid (value axis only)
  valGridLine: { color: "E2E8F0", size: 0.5 },
  catGridLine: { style: "none" },

  // Data labels on bars
  showValue: true,
  dataLabelPosition: "outEnd",
  dataLabelColor: "1E293B",

  // Hide legend for single series
  showLegend: false,
});
```

**Key styling options:**
- `chartColors: [...]` - hex colors for series/segments
- `chartArea: { fill, border, roundedCorners }` - chart background
- `catGridLine/valGridLine: { color, style, size }` - grid lines (`style: "none"` to hide)
- `lineSmooth: true` - curved lines (line charts)
- `legendPos: "r"` - legend position: "b", "t", "l", "r", "tr"

---

## Slide Masters

```javascript
pres.defineSlideMaster({
  title: 'TITLE_SLIDE', background: { color: '283A5E' },
  objects: [{
    placeholder: { options: { name: 'title', type: 'title', x: 1, y: 2, w: 8, h: 2 } }
  }]
});

let titleSlide = pres.addSlide({ masterName: "TITLE_SLIDE" });
titleSlide.addText("My Title", { placeholder: "title" });
```

---

## Common Pitfalls

⚠️ These issues cause file corruption, visual bugs, or broken output. Avoid them.

1. **NEVER use "#" with hex colors** - causes file corruption
   ```javascript
   color: "FF0000"      // ✅ CORRECT
   color: "#FF0000"     // ❌ WRONG
   ```

2. **NEVER encode opacity in hex color strings** - 8-char colors (e.g., `"00000020"`) corrupt the file. Use the `opacity` property instead.
   ```javascript
   shadow: { type: "outer", blur: 6, offset: 2, color: "00000020" }          // ❌ CORRUPTS FILE
   shadow: { type: "outer", blur: 6, offset: 2, color: "000000", opacity: 0.12 }  // ✅ CORRECT
   ```

3. **Use `bullet: true`** - NEVER unicode symbols like "•" (creates double bullets)

4. **Use `breakLine: true`** between array items or text runs together

5. **Avoid `lineSpacing` with bullets** - causes excessive gaps; use `paraSpaceAfter` instead

6. **Each presentation needs fresh instance** - don't reuse `pptxgen()` objects

7. **NEVER reuse option objects across calls** - PptxGenJS mutates objects in-place (e.g. converting shadow values to EMU). Sharing one object between multiple calls corrupts the second shape.
   ```javascript
   const shadow = { type: "outer", blur: 6, offset: 2, color: "000000", opacity: 0.15 };
   slide.addShape(pres.shapes.RECTANGLE, { shadow, ... });  // ❌ second call gets already-converted values
   slide.addShape(pres.shapes.RECTANGLE, { shadow, ... });

   const makeShadow = () => ({ type: "outer", blur: 6, offset: 2, color: "000000", opacity: 0.15 });
   slide.addShape(pres.shapes.RECTANGLE, { shadow: makeShadow(), ... });  // ✅ fresh object each time
   slide.addShape(pres.shapes.RECTANGLE, { shadow: makeShadow(), ... });
   ```

8. **Don't use `ROUNDED_RECTANGLE` with accent borders** - rectangular overlay bars won't cover rounded corners. Use `RECTANGLE` instead.
   ```javascript
   // ❌ WRONG: Accent bar doesn't cover rounded corners
   slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 1, y: 1, w: 3, h: 1.5, fill: { color: "FFFFFF" } });
   slide.addShape(pres.shapes.RECTANGLE, { x: 1, y: 1, w: 0.08, h: 1.5, fill: { color: "0891B2" } });

   // ✅ CORRECT: Use RECTANGLE for clean alignment
   slide.addShape(pres.shapes.RECTANGLE, { x: 1, y: 1, w: 3, h: 1.5, fill: { color: "FFFFFF" } });
   slide.addShape(pres.shapes.RECTANGLE, { x: 1, y: 1, w: 0.08, h: 1.5, fill: { color: "0891B2" } });
   ```

---

## Speaker Script

When creating a presentation from scratch, **also generate a companion speaker script** (`SPEAKER_SCRIPT.md`) alongside the `.pptx`. See [SKILL.md § Speaker Script](SKILL.md#speaker-script) for the full format, guidelines, and demo section details.

Key points:
- Write in conversational spoken tone (contractions, rhetorical questions)
- Use `>` blockquotes for actual narration
- Add `### 🖥️ DEMO:` sections after theory slides with exact run commands and expected outputs
- Read the actual source to describe specific demo behaviors accurately
- End each slide section with a natural transition to the next

---

## Quick Reference

- **Shapes**: RECTANGLE, OVAL, LINE, ROUNDED_RECTANGLE
- **Charts**: BAR, LINE, PIE, DOUGHNUT, SCATTER, BUBBLE, RADAR
- **Layouts**: LAYOUT_16x9 (10"×5.625"), LAYOUT_16x10, LAYOUT_4x3, LAYOUT_WIDE
- **Alignment**: "left", "center", "right"
- **Chart data labels**: "outEnd", "inEnd", "center"
