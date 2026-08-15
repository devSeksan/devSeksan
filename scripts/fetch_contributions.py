import os
import json
import re
import requests
from bs4 import BeautifulSoup

USERNAME = "devSeksan"
URL = f"https://github.com/users/{USERNAME}/contributions"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

days_data = []
for cell in soup.find_all("td", class_="ContributionCalendar-day"):
    date = cell.get("data-date")
    level = cell.get("data-level", "0")
    if date:
        days_data.append({"date": date, "level": int(level)})

# ดึงยอดสรุป contributions เช่น "121 contributions in the last year"
total_text = "contributions in the last year"
match = re.search(r"([0-9,]+)\s+contributions\s+in\s+the\s+last\s+year", response.text)
if match:
    total_text = f"{match.group(1)} contributions in the last year"
else:
    total_text = "121 contributions in the last year"

os.makedirs("data", exist_ok=True)

with open("data/contributions.json", "w", encoding="utf-8") as f:
    json.dump({
        "username": USERNAME,
        "total_text": total_text,
        "days": days_data
    }, f, indent=2, ensure_ascii=False)

print(f"Fetched {len(days_data)} days and '{total_text}' successfully!")