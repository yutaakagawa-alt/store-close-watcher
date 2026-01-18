import requests
import os
import subprocess
from bs4 import BeautifulSoup

QUERY = "閉店"
MAX_RESULTS = 5
SENT_FILE = "sent_x.txt"

LINE_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

# Nitter（Xミラー）
BASE_URL = "https://nitter.net/search"

def load_sent():
    if not os.path.exists(SENT_FILE):
        return set()
    with open(SENT_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())

def save_sent(urls):
    with open(SENT_FILE, "w", encoding="utf-8") as f:
        for u in sorted(urls):
            f.write(u + "\n")

def send_line(msg):
    url = "https://api.line.me/v2/bot/message/broadcast"
    headers = {
        "Authorization": f"Bearer {LINE_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {"messages": [{"type": "text", "text": msg}]}
    requests.post(url, headers=headers, json=data)

print("Searching X (via Nitter)...")

res = requests.get(
    BASE_URL,
    params={"q": QUERY, "f": "tweets"},
    headers={"User-Agent": "Mozilla/5.0"}
)

print("HTTP STATUS:", res.status_code)
print("HTML LENGTH:", len(res.text))

soup = BeautifulSoup(res.text, "html.parser")

tweets = []
for item in soup.select(".timeline-item"):
    content = item.select_one(".tweet-content")
    link = item.select_one("a.tweet-link")
    if content and link:
        text = content.get_text(strip=True)
        url = "https://nitter.net" + link.get("href")
        tweets.append((text, url))
    if len(tweets) >= MAX_RESULTS:
        break

sent = load_sent()
new_items = [(t, u) for t, u in tweets if u not in sent]

print("X results:")
for t, u in tweets:
    print("-", t[:50])
    print(" ", u)

if not new_items:
    print("新規ツイートなし。送信しません。")
    exit(0)

message = "【新規 X 閉店情報】\n"
for t, u in new_items:
    message += f"\n{t}\n{u}\n"
    sent.add(u)

send_line(message)
save_sent(sent)

# GitHubに保存
subprocess.run(["git", "config", "--global", "user.name", "github-actions"])
subprocess.run(["git", "config", "--global", "user.email", "actions@github.com"])
subprocess.run(["git", "add", SENT_FILE])
subprocess.run(["git", "commit", "-m", "Update sent X URLs"])
subprocess.run(["git", "push"])
