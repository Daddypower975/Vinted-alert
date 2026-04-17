import requests
import time

TELEGRAM_TOKEN = "8296587636:AAGqu41JLNbBVTw8oPjPrhULeQuazDC5P5Q"
CHAT_ID = "5723752685"

VINTED_SESSION =  "bk0rZUZlMEtGdlVkWjhUMDlHblFaVVJRV2JES2EvSVNWVzJyTjN4MFBUbnVXTnFDVWNmZ1oza0ZVMS8xaElHL0JSclpHcVZrMlpZQlRDL1hrOXpPVFVJN0xZcUZwVGp4Qzk1azlPVk5lc2R5anMwb3dXNkxsLy9pNVJaa1J5NWJBTVJQNnFVVkJJa05FOVJhT2hEWS81aGxBZDY1YVgrZTBESXhLd3ZlRUdDekhEbEVjWDhnMGdud2VObmxXdXdwTE4wZFp0RmpucThLYzY3VU9TdG1qZGgyR3VzQkkzZEZwVklncVFzQXRFL2NJdW0rRUFlOWNPVkRrUGxxaVVaTy0tV3NwQ1lPVVhwNXVackVPNTJUK0cyZz09--c01ab48a3eb88371a3f7f005f7764ee588efb8b2"

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
    r = requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    print("Telegram response:", r.status_code, r.text)

def check_vinted(query):
    url = f"https://www.vinted.fr/api/v2/catalog/items?search_text={query}&per_page=20"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "fr-FR,fr;q=0.9",
        "Referer": "https://www.vinted.fr/",
        "Origin": "https://www.vinted.fr",
        "Cookie": f"_vinted_fr_session={VINTED_SESSION}"
    }
    
    r = requests.get(url, headers=headers, timeout=10)
    print(f"Vinted [{query}]: {r.status_code}")
    
    if r.status_code != 200 or not r.text:
        print(f"Bloqué ou réponse vide pour: {query}")
        return
    
    items = r.json().get("items", [])
    for item in items:
        if item["id"] not in seen_ids:
            seen_ids.add(item["id"])
            msg = f"🔔 Nouveau sur Vinted !\n{item['title']}\n{item['price']} €\n{item['url']}"
            send_telegram(msg)

print("Démarrage...")
send_telegram("✅ Bot Vinted démarré !")

while True:
    for q in SEARCHES:
        check_vinted(q)
        time.sleep(10)  # pause entre chaque recherche
    time.sleep(300)
