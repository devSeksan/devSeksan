import json

with open("data/contributions.json") as f:
    data = json.load(f)

days = data.get("days", [])
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

# สร้าง SVG พร้อม Animation สไลด์ไล่จากซ้ายไปขวา
svg_elements = []
for i, day in enumerate(days[-371:]):  # ดึง 53 สัปดาห์ล่าสุด (53*7 = 371 วัน)
    col = i // 7
    row = i % 7
    x = col * 15 + 15
    y = row * 15 + 30
    color = PALETTE[day["level"]]
    delay = (col * 0.02) + (row * 0.01)

    svg_elements.append(
        f'<rect x="{x}" y="{y}" width="11" height="11" rx="2" fill="{color}" opacity="0">'
        f'<animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="{delay:.2f}s" fill="freeze" />'
        f'<animateTransform attributeName="transform" type="translate" from="0 -10" to="0 0" dur="0.4s" begin="{delay:.2f}s" fill="freeze" />'
        f'</rect>'
    )

svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="860" height="150" viewBox="0 0 860 150">
  <style>
    .bg {{ fill: #0d1117; stroke: #30363d; rx: 10px; }}
    .title {{ font-family: monospace; font-size: 12px; fill: #7ee787; }}
  </style>
  <rect width="860" height="150" class="bg" />
  <text x="20" y="20" class="title">🔴 🟡 🟢  zsh — devSeksan@github:~$ ./contributions.sh</text>
  {''.join(svg_elements)}
</svg>"""

with open("contrib-heatmap.svg", "w", encoding="utf-8") as f:
    f.write(svg_content)

print("Generated contrib-heatmap.svg successfully!")