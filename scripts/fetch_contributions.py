import os
import json
import requests
from bs4 import BeautifulSoup

USERNAME = "devSeksan"
URL = f"https://github.com/users/{USERNAME}/contributions"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

days_data = []
for cell in soup.find_all("td", class_="ContributionCalendar-day"):
    date = cell.get("data-date")
    level = cell.get("data-level", "0")
    if date:
        days_data.append({"date": date, "level": int(level)})

# สร้างโฟลเดอร์ data อัตโนมัติหากยังไม่มี
os.makedirs("data", exist_ok=True)

with open("data/contributions.json", "w", encoding="utf-8") as f:
    json.dump({"username": USERNAME, "days": days_data}, f, indent=2)

print(f"Fetched {len(days_data)} days of contributions successfully!")