import requests
from bs4 import BeautifulSoup

query = "TSUTAYA 閉店 福岡"
URL = f"https://www.google.com/search?q={query}"

res = requests.get(URL, headers={
    "User-Agent": "Mozilla/5.0"
})

soup = BeautifulSoup(res.text, "html.parser")

print("Google results:")
for a in soup.select("a"):
    href = a.get("href", "")
    if href.startswith("/url?q="):
        link = href.split("/url?q=")[1].split("&")[0]
        if "google" not in link:
            print(link)
