import os
import json
import re
import datetime
import requests
from bs4 import BeautifulSoup

USERNAME = "devSeksan"
URL = f"https://github.com/users/{USERNAME}/contributions"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

days_dict = {}

# ดึงข้อมูลจากตาราง GitHub
for cell in soup.find_all("td", class_="ContributionCalendar-day"):
    date = cell.get("data-date")
    level = int(cell.get("data-level", "0"))
    if date:
        # กำหนดจำนวนคร่าวๆ ตาม level หากไม่มี tooltip
        count = [0, 1, 6, 16, 31, 50][min(level, 5)]
        days_dict[date] = {"date": date, "count": count, "level": level}

# สแครปจำนวนจริงจาก tooltip (ถ้ามี)
for tip in soup.find_all(["tool-tip", "div"], id=re.compile(r"contribution-day-component")):
    text = tip.get_text()
    for date in days_dict:
        if date in text:
            m = re.search(r"(\d+)\s+contribution", text)
            if m:
                days_dict[date]["count"] = int(m.group(1))

# เรียงลำดับตามวันที่
days_data = sorted(days_dict.values(), key=lambda x: x["date"])

# คำนวณสถิติ
total_contributions = sum(d["count"] for d in days_data)
best_day = max(days_data, key=lambda x: x["count"], default={"count": 0, "date": "N/A"})

longest_streak = 0
current_streak = 0
temp_streak = 0

for d in days_data:
    if d["count"] > 0:
        temp_streak += 1
        longest_streak = max(longest_streak, temp_streak)
    else:
        temp_streak = 0

for d in reversed(days_data):
    if d["count"] > 0:
        current_streak += 1
    else:
        break

payload = {
    "username": USERNAME,
    "total_contributions": total_contributions,
    "best_day": {"count": best_day["count"], "date": best_day["date"]},
    "current_streak": {"length": current_streak},
    "longest_streak": {"length": longest_streak},
    "range": {
        "start": days_data[0]["date"] if days_data else "N/A",
        "end": days_data[-1]["date"] if days_data else "N/A"
    },
    "days": days_data
}

os.makedirs("data", exist_ok=True)
with open("data/contributions.json", "w", encoding="utf-8") as f:
    json.dump(payload, f, indent=2, ensure_ascii=False)

print(f"Fetched {len(days_data)} days, Total: {total_contributions}, Best: {best_day['count']}")