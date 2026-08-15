cat_ascii = [
    "         /\\_/\\          ",
    "        ( o.o )  ☕     ",
    "        >  ^  <  [~]    ",
    "       /       \\  |     ",
    "      (  | | |  ) |     ",
    "     (___| | |___/      ",
    "   =================    ",
    "   | devSeksan's Dev |   ",
    "   =================    ",
]

lines_svg = []
for i, line in enumerate(cat_ascii):
    delay = i * 0.08
    y = 55 + (i * 22)
    lines_svg.append(
        f'<text x="25" y="{y}" class="ascii-line" style="animation-delay: {delay:.2f}s;">{line}</text>'
    )

svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="370" height="340" viewBox="0 0 370 340">
  <style>
    .bg {{ fill: #0d1117; stroke: #30363d; stroke-width: 1; rx: 8px; }}
    .title {{ font-family: monospace; font-size: 12px; fill: #58a6ff; }}
    .ascii-line {{
      font-family: "Courier New", Courier, monospace;
      font-size: 14px;
      font-weight: bold;
      fill: #58a6ff;
      white-space: pre;
      opacity: 0;
      animation: typeIn 0.3s ease-out forwards;
    }}
    @keyframes typeIn {{
      from {{ opacity: 0; transform: translateX(-6px); }}
      to {{ opacity: 1; transform: translateX(0); }}
    }}
  </style>

  <rect width="370" height="340" class="bg" />
  <text x="16" y="24" class="title">🔴 🟡 🟢  cat_avatar.sh</text>

  {''.join(lines_svg)}
</svg>"""

with open("avi-ascii.svg", "w", encoding="utf-8") as f:
    f.write(svg_content)

print("Generated avi-ascii.svg successfully!")