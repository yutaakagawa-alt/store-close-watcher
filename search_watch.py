import requests
from bs4 import BeautifulSoup

# ===== 設定 =====
QUERY = "閉店 店舗"
MAX_RESULTS = 10

# DuckDuckGo HTML版（重要）
URL = "https://duckduckgo.com/html/"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# ===== 検索実行 =====
response = requests.get(
    URL,
    params={"q": QUERY},
    headers=HEADERS,
    timeout=20
)

print("HTTP STATUS:", response.status_code)
print("HTML LENGTH:", len(response.text))

soup = BeautifulSoup(response.text, "html.parser")

# ===== 結果抽出 =====
links = []

for a in soup.select("a.result__a"):
    title = a.get_text(strip=True)
    link = a.get("href")
    if title and link:
        links.append((title, link))

# ===== 表示 =====
print("DuckDuckGo results:")
if not links:
    print("（結果なし）")

for title, link in links[:MAX_RESULTS]:
    print(f"- {title}")
    print(f"  {link}")
