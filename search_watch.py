import requests
from bs4 import BeautifulSoup

QUERY = "閉店"
MAX_RESULTS = 10

url = "https://html.duckduckgo.com/html/"
params = {
    "q": QUERY
}

headers = {
    "User-Agent": "Mozilla/5.0"
}

# --- ① まず検索ページを取得 ---
response = requests.post(url, data=params, headers=headers)
html = response.text

# ★★★ ここに入れる ★★★
print("HTML LENGTH:", len(html))
print(html[:500])
# ★★★ ここまで ★★★

# --- ② HTMLを解析 ---
soup = BeautifulSoup(html, "html.parser")

links = []
for a in soup.select("a.result__a"):
    title = a.get_text(strip=True)
    link = a.get("href")
    if title and link:
        links.append((title, link))

# --- ③ 結果表示 ---
print("DuckDuckGo results:")
for title, link in links[:MAX_RESULTS]:
    print(f"- {title}")
    print(f"  {link}")
