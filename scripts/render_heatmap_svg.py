import json
import datetime

with open("data/contributions.json", encoding="utf-8") as f:
    data = json.load(f)

# ดึง 53 สัปดาห์ล่าสุด (53 * 7 = 371 วัน)
days = data.get("days", [])[-371:]
total_text = data.get("total_text", "133 contributions in the last year")

# โทนสีเขียวตามแบบฉบับของ GitHub
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

START_X = 38
START_Y = 28
CELL_SIZE = 11
CELL_GAP = 4
STEP = CELL_SIZE + CELL_GAP  # 15px

# 1. คำนวณตำแหน่งชื่อเดือนตามสัปดาห์จริง
month_labels = []
if days:
    first_month = datetime.date.fromisoformat(days[0]["date"]).month
    month_labels.append((START_X, MONTH_NAMES[first_month - 1]))
    last_m = first_month

    for col in range(1, 53):
        week_days = days[col * 7 : (col + 1) * 7]
        for d in week_days:
            d_obj = datetime.date.fromisoformat(d["date"])
            if d_obj.day <= 7 and d_obj.month != last_m and col < 51:
                x = START_X + col * STEP
                month_labels.append((x, MONTH_NAMES[d_obj.month - 1]))
                last_m = d_obj.month
                break

month_svg = "".join([f'<text x="{mx}" y="15" class="label">{mname}</text>' for mx, mname in month_labels])

# 2. วาดตารางช่องสี่เหลี่ยมโค้งมน พร้อมแอนิเมชันเลื่อนในแนวทแยง
svg_cells = []
for i, day in enumerate(days):
    col = i // 7
    row = i % 7
    x = START_X + col * STEP
    y = START_Y + row * STEP
    lvl = day.get("level", 0)
    color = PALETTE[min(lvl, len(PALETTE) - 1)]
    delay = (col * 0.012) + (row * 0.02)
    
    svg_cells.append(
        f'<rect x="{x}" y="{y}" width="{CELL_SIZE}" height="{CELL_SIZE}" rx="2.5" fill="{color}" opacity="0">'
        f'<animate attributeName="opacity" from="0" to="1" dur="0.3s" begin="{delay:.2f}s" fill="freeze" />'
        f'<animateTransform attributeName="transform" type="translate" from="0 -5" to="0 0" dur="0.3s" begin="{delay:.2f}s" fill="freeze" />'
        f'</rect>'
    )

# 3. จัดตัวเลขยอดสรุปให้เป็นสีขาวตัวหนา
parts = total_text.split(" ", 1)
if len(parts) == 2:
    total_svg = f'<tspan font-weight="700" fill="#f0f6fc">{parts[0]}</tspan> <tspan fill="#8b949e">{parts[1]}</tspan>'
else:
    total_svg = f'<tspan font-weight="700" fill="#f0f6fc">{total_text}</tspan>'

heatmap_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="860" height="165" viewBox="0 0 860 165" fill="none">
  <style>
    .label {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
      font-size: 10px;
      fill: #7d8590;
    }}
    .footer-text {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
      font-size: 12px;
    }}
  </style>

  <!-- Month Labels -->
  {month_svg}

  <!-- Day Labels -->
  <text x="10" y="{START_Y + 1 * STEP + 9}" class="label">Mon</text>
  <text x="10" y="{START_Y + 3 * STEP + 9}" class="label">Wed</text>
  <text x="10" y="{START_Y + 5 * STEP + 9}" class="label">Fri</text>

  <!-- Grid of Contribution Cells -->
  {''.join(svg_cells)}

  <!-- Footer Total Text -->
  <text x="{START_X}" y="{START_Y + 7 * STEP + 20}" class="footer-text">
    {total_svg}
  </text>
</svg>"""

with open("contrib-heatmap.svg", "w", encoding="utf-8") as f:
    f.write(heatmap_svg)

print("Generated contrib-heatmap.svg successfully!")