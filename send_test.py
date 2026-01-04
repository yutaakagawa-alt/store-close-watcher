import os
import requests

TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
USER_ID = "U2322fdfe339ffeab7c74bc77c681fa14"  # ← 自分のものに置き換え

url = "https://api.line.me/v2/bot/message/push"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

payload = {
    "to": USER_ID,
    "messages": [
        {"type": "text", "text": "🎉 最終テスト：LINE送信成功！"}
    ]
}

res = requests.post(url, headers=headers, json=payload)
print(res.status_code)
print(res.text)
