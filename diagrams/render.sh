#!/bin/bash
# Render all Mermaid diagrams to PNG
set -e
cd "$(dirname "$0")"
CFG="mermaid.config.json"

echo "Rendering diagrams..."

# All diagrams — wide viewport for landscape-friendly output
for f in module01_stateless module03_rag module04_tools module05_react module07_pipeline module08_context module09_mcp module10_stack; do
    echo "  $f..."
    mmdc -i "${f}.mmd" -o "${f}.png" -c "$CFG" -w 900 -H 440 -b transparent
done

echo "Done! All PNGs written to diagrams/"
