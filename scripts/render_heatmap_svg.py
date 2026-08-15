import json

with open("data/contributions.json", encoding="utf-8") as f:
    data = json.load(f)

days = data.get("days", [])[-371:]  # 53 สัปดาห์
total_text = data.get("total_text", "121 contributions in the last year")

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
MONTH_NAMES = ["Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug"]

START_X = 42
START_Y = 28
CELL_SIZE = 11
CELL_GAP = 4
STEP = CELL_SIZE + CELL_GAP  # 15px

svg_cells = []
for i, day in enumerate(days):
    col = i // 7
    row = i % 7
    x = START_X + col * STEP
    y = START_Y + row * STEP
    lvl = day.get("level", 0)
    color = PALETTE[min(lvl, len(PALETTE) - 1)]
    delay = (col * 0.015) + (row * 0.02)
    
    svg_cells.append(
        f'<rect x="{x}" y="{y}" width="{CELL_SIZE}" height="{CELL_SIZE}" rx="2" fill="{color}" opacity="0">'
        f'<animate attributeName="opacity" from="0" to="1" dur="0.35s" begin="{delay:.2f}s" fill="freeze" />'
        f'<animateTransform attributeName="transform" type="translate" from="0 -6" to="0 0" dur="0.35s" begin="{delay:.2f}s" fill="freeze" />'
        f'</rect>'
    )

# คำนวณตำแหน่งเดือน
month_positions = [
    (42 + int(col_idx * 4.41 * STEP), MONTH_NAMES[col_idx % len(MONTH_NAMES)])
    for col_idx in range(13)
]
month_svg = "".join([f'<text x="{mx}" y="16" class="label">{mname}</text>' for mx, mname in month_positions[:12]])

# จัดฟอร์แมตตัวเลขหนา
parts = total_text.split(" ", 1)
if len(parts) == 2:
    total_svg = f'<tspan font-weight="600" fill="#f0f6fc">{parts[0]}</tspan> <tspan fill="#8b949e">{parts[1]}</tspan>'
else:
    total_svg = f'<tspan font-weight="600" fill="#f0f6fc">{total_text}</tspan>'

heatmap_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="860" height="170" viewBox="0 0 860 170" fill="none">
  <style>
    .label {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
      font-size: 10.5px;
      fill: #7d8590;
    }}
    .footer-text {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
      font-size: 12.5px;
    }}
  </style>
  
  <!-- Month Labels -->
  {month_svg}
  
  <!-- Day Labels -->
  <text x="12" y="{START_Y + 1 * STEP + 9}" class="label">Mon</text>
  <text x="12" y="{START_Y + 3 * STEP + 9}" class="label">Wed</text>
  <text x="12" y="{START_Y + 5 * STEP + 9}" class="label">Fri</text>

  <!-- Heatmap Cells -->
  {''.join(svg_cells)}

  <!-- Footer Total Contributions -->
  <text x="{START_X}" y="{START_Y + 7 * STEP + 22}" class="footer-text">
    {total_svg}
  </text>
</svg>"""

with open("contrib-heatmap.svg", "w", encoding="utf-8") as f:
    f.write(heatmap_svg)

print("Generated contrib-heatmap.svg successfully!")