import os
import requests


TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]


def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    response = requests.post(
        url,
        json=payload,
        timeout=10
    )

    print("HTTP Status:", response.status_code)

    response.raise_for_status()


message = """
🚨 智慧通勤通知測試

這是一則 GitHub Actions 測試訊息。

如果你看到這則訊息，
代表 Telegram Bot 設定成功！
"""

send_telegram(message)
