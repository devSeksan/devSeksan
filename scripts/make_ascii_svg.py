ascii_rows = [
    "                 .---.                  ",
    "                /     \\                 ",
    "               | () () |   ☕           ",
    "                \\  _  /   [~]           ",
    "        .---.____/     \\____.---.       ",
    "       /  /      \\     /     \\  \\       ",
    "      |  |   ( )  \\   /  ( )  |  |      ",
    "      |  |         | |        |  |      ",
    "      |  |    ___  | |  ___   |  |      ",
    "      \\  \\   (   ) | | (   )  /  /      ",
    "       '--'\\  \\ /  | |  \\ /  / '--'     ",
    "            \\__\\___|_|___/__/           ",
    "             |  |  ===== |  |           ",
    "             |  |  ----- |  |           ",
    "             |  |________|  |           ",
    "             /               \\          ",
    "            /  devseksan.dev  \\         ",
    "           /___________________\\        ",
]

rows_svg = []
for i, r in enumerate(ascii_rows):
    delay = i * 0.04
    y = 60 + (i * 15.5)
    rows_svg.append(
        f'<text x="24" y="{y:.1f}" class="ascii-line" style="animation-delay: {delay:.2f}s;">{r}</text>'
    )

svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="370" height="375" viewBox="0 0 370 375">
  <style>
    .bg {{ fill: #0d1117; stroke: #30363d; stroke-width: 1; rx: 8px; }}
    .title {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", monospace; font-size: 11px; fill: #7d8590; }}
    .ascii-line {{
      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
      font-size: 12.5px;
      font-weight: 500;
      fill: #e6edf3;
      white-space: pre;
      opacity: 0;
      animation: fadeInRow 0.25s ease-out forwards;
    }}
    .footer-prompt {{
      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
      font-size: 11px;
      fill: #8b949e;
    }}
    .footer-val {{ fill: #58a6ff; font-weight: bold; }}
    @keyframes fadeInRow {{
      from {{ opacity: 0; transform: translateY(-3px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}
  </style>

  <rect width="370" height="375" class="bg" />
  
  <!-- Mac Window Dots & Title -->
  <circle cx="18" cy="18" r="4.5" fill="#ff5f56" />
  <circle cx="32" cy="18" r="4.5" fill="#ffbd2e" />
  <circle cx="46" cy="18" r="4.5" fill="#27c93f" />
  <text x="185" y="21" class="title" text-anchor="middle">devSeksan@github: ~$ ./portrait.sh</text>

  <!-- ASCII Art Body -->
  {''.join(rows_svg)}

  <!-- Footer Prompt -->
  <text x="24" y="354" class="footer-prompt">
    devSeksan@github:~$ whoami <tspan class="footer-val">Seksan</tspan>
  </text>
</svg>"""

with open("avi-ascii.svg", "w", encoding="utf-8") as f:
    f.write(svg_content)

print("Generated avi-ascii.svg successfully!")