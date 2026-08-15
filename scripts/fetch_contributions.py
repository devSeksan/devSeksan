import json
import requests
from bs4 import BeautifulSoup

USERNAME = "devSeksan"  # ใส่ Username ของคุณ
URL = f"https://github.com/users/{USERNAME}/contributions"

response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

days_data = []
for cell in soup.find_all("td", class_="ContributionCalendar-day"):
    date = cell.get("data-date")
    level = cell.get("data-level", "0")
    if date:
        days_data.append({"date": date, "level": int(level)})

with open("data/contributions.json", "w") as f:
    json.dump({"username": USERNAME, "days": days_data}, f, indent=2)

print("Fetched contributions successfully!")