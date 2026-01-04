import requests
import os

LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
USER_ID = os.environ.get("LINE_USER_ID")

url = "https://api.line.me/v2/bot/message/push"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
}

data = {
    "to": USER_ID,
    "messages": [
        {
            "type": "text",
            "text": "✅ LINE通知テスト成功です"
        }
    ]
}

response = requests.post(url, headers=headers, json=data)
print(response.status_code, response.text)
