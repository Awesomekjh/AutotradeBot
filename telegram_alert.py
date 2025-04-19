# telegram_alert.py

import requests
import json

with open("AHA_X_Strategy/config.json", "r") as f:
    config = json.load(f)

TOKEN = config["telegram_token"]
CHAT_ID = config["telegram_chat_id"]

def send_alert(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"[ERROR] 텔레그램 전송 실패: {e}")
