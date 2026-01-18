import requests
from bs4 import BeautifulSoup
import os
import json

# =========================
# 設定
# =========================
QUERY = "閉店"
MAX_RESULTS = 10
SAVE_FILE = "last_results.txt"

DUCK_URL = "https://lite.duckduckgo.com/lite/"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

LINE_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
LINE_PUSH_URL = "https://api.line.me/v2/bot/message/push"
USER_ID = os.environ.get("LINE_USER_ID")

# =========================
# DuckDuckGo 検索
# =========================
response = requests.post(
    DUCK_URL,
    data={"q": QUERY},
    headers=HEADERS,
    timeout=20
)

print("HTTP STATUS:", response.status_code)
html = response.text
print("HTML LENGTH:", len(html))

soup = BeautifulSoup(html, "html.parser")

links = []
for a in soup.select("a.result-link"):
    title = a.get_text(strip=True)
    link = a.get("href")
    if title and link:
        links.append((title, link))

print("DuckDuckGo results:")
for title, link in links[:MAX_RESULTS]:
    print(f"- {title}")
    print(f"  {link}")

# =========================
# 前回結果の読み込み
# =========================
old_links = set()
if os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        for line in f:
            old_links.add(line.strip())

# =========================
# 差分検出
# =========================
current_links = set(link for _, link in links[:MAX_RESULTS])
new_links = current_links - old_links

print("----")
if new_links:
    print("NEW RESULTS:")
    for link in new_links:
        print(link)
else:
    print("（新着なし）")

# =========================
# LINE 通知
# =========================
if new_links and LINE_TOKEN and USER_ID:
    message = "【閉店 新着検出】\n" + "\n".join(new_links)

    payload = {
        "to": USER_ID,
        "messages": [
            {"type": "text", "text": message}
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_TOKEN}"
    }

    r = requests.post(
        LINE_PUSH_URL,
        headers=headers,
        data=json.dumps(payload)
    )

    print("LINE PUSH STATUS:", r.status_code)
else:
    print("LINE送信なし（新着なし or 環境変数未設定）")

# =========================
# 今回結果を保存
# =========================
with open(SAVE_FILE, "w", encoding="utf-8") as f:
    for link in current_links:
        f.write(link + "\n")
