import requests
from bs4 import BeautifulSoup

QUERY = "閉店 お知らせ 店舗"
MAX_RESULTS = 10

url = "https://duckduckgo.com/html/"
params = {
    "q": QUERY,
    "kl": "jp-jp"
}

headers = {
    "User-Agent": "Mozilla/5.0"
}

res = requests.post(url, data=params, headers=headers, timeout=15)
res.raise_for_status()

soup = BeautifulSoup(res.text, "html.parser")

links = []
for a in soup.select("a.result__a"):
    href = a.get("href")
    title = a.get_text(strip=True)
    if href:
        links.append((title, href))

print("DuckDuckGo results:")
for title, link in links[:MAX_RESULTS]:
    print(f"- {title}")
    print(f"  {link}")
