import requests
from bs4 import BeautifulSoup

URL = "https://x.com/search?q=TSUTAYA 閉店&f=live"

res = requests.get(URL, headers={
    "User-Agent": "Mozilla/5.0"
})

soup = BeautifulSoup(res.text, "html.parser")

links = set()
for a in soup.find_all("a", href=True):
    if "/status/" in a["href"]:
        links.add("https://x.com" + a["href"])

print("X results:")
for link in list(links)[:5]:
    print(link)
