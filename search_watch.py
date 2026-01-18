import requests
from bs4 import BeautifulSoup

# ===== 設定 =====
QUERY = "閉店 店舗"
MAX_RESULTS = 10

# DuckDuckGo LITE（重要）
URL = "https://lite.duckduckgo.com/lite/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# ===== 検索実行 =====
response = requests.post(
    URL,
    data={"q": QUERY},
    headers=HEADERS,
    timeout=20
)

print("HTTP STATUS:", response.status_code)
print("HTML LENGTH:", len(response.text))

soup = BeautifulSoup(response.text, "html.parser")

# ===== 結果抽出 =====
links = []

for a in soup.select("a"):
    href = a.get("href")
    title = a.get_text(strip=True)
    if href and title and href.startswith("http"):
        links.append((title, href))

# ===== 表示 =====
print("DuckDuckGo results:")
if not links:
    print("（結果なし）")

for title, link in links[:MAX_RESULTS]:
    print(f"- {title}")
    print(f"  {link}")
