import requests
import time
import json
import os

TELEGRAM_TOKEN = "8296587636:AAEJfUT0VTGPxUIQXbFiNVV9i0OYl_khBdo"
CHAT_ID = "5723752685"

SEARCHES = [
    "Urban Comics",
    "Dumezil",
    "Tempus",
    "Perrin",
    "Edition delga"
]

seen_ids = set()

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def check_vinted(query):
    url = f"https://www.vinted.fr/api/v2/catalog/items?search_text={query}&per_page=20"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        items = r.json().get("items", [])
        for item in items:
            if item["id"] not in seen_ids:
                seen_ids.add(item["id"])
                msg = f"🔔 Nouveau sur Vinted !\n{item['title']}\n{item['price']} €\n{item['url']}"
                send_telegram(msg)
    except:
        pass

send_telegram("✅ Bot Vinted démarré !")

while True:
    for q in SEARCHES:
        check_vinted(q)
    time.sleep(300)
