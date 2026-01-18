import requests
import os
import subprocess
from bs4 import BeautifulSoup

SEARCH_URL = "https://duckduckgo.com/html/"
QUERY = "閉店"
MAX_RESULTS = 5
SENT_FILE = "sent_urls.txt"

LINE_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

def load_sent_urls():
    if not os.path.exists(SENT_FILE):
        return set()
    with open(SENT_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())

def save_sent_urls(urls):
    with open(SENT_FILE, "w", encoding="utf-8") as f:
        for url in sorted(urls):
            f.write(url + "\n")

def send_line(message):
    url = "https://api.line.me/v2/bot/message/broadcast"
    headers = {
        "Authorization": f"Bearer {LINE_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messages": [{"type": "text", "text": message}]
    }
    requests.post(url, headers=headers, json=data)

print("Searching DuckDuckGo...")

res = requests.post(
    SEARCH_URL,
    data={"q": QUERY, "kl": "jp-jp"},
    headers={"User-Agent": "Mozilla/5.0"}
)

print("HTTP STATUS:", res.status_code)
print("HTML LENGTH:", len(res.text))

soup = BeautifulSoup(res.text, "html.parser")

results = []
for a in soup.select("a.result__a"):
    title = a.get_text(strip=True)
    link = a.get("href")
    if link:
        results.append((title, link))
    if len(results) >= MAX_RESULTS:
        break

sent_urls = load_sent_urls()
new_items = [(t, l) for t, l in results if l not in sent_urls]

print("DuckDuckGo results:")
for t, l in results:
    print("-", t)
    print(" ", l)

if not new_items:
    print("新規URLなし。送信しません。")
    exit(0)

message = "【新規 閉店情報】\n"
for t, l in new_items:
    message += f"\n{t}\n{l}\n"
    sent_urls.add(l)

send_line(message)
save_sent_urls(sent_urls)

# GitHubに保存
subprocess.run(["git", "config", "--global", "user.name", "github-actions"])
subprocess.run(["git", "config", "--global", "user.email", "actions@github.com"])
subprocess.run(["git", "add", SENT_FILE])
subprocess.run(["git", "commit", "-m", "Update sent URLs"])
subprocess.run(["git", "push"])
