import requests
from bs4 import BeautifulSoup
import os

# =========================
# 設定
# =========================
QUERY = "閉店"
MAX_RESULTS = 10
SAVE_FILE = "last_results.txt"

URL = "https://lite.duckduckgo.com/lite/"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# =========================
# DuckDuckGo 検索
# =========================
response = requests.post(
    URL,
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

# =========================
# 結果表示
# =========================
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
# 今回結果との差分
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
# 今回結果を保存
# =========================
with open(SAVE_FILE, "w", encoding="utf-8") as f:
    for link in current_links:
        f.write(link + "\n")
