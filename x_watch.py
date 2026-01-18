import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def google_search(query):
    url = "https://www.google.com/search"
    params = {"q": query, "hl": "ja"}
    r = requests.get(url, params=params, headers=HEADERS, timeout=10)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    links = []

    for a in soup.select("a"):
        href = a.get("href")
        if href and href.startswith("/url?q="):
            link = href.split("/url?q=")[1].split("&")[0]
            links.append(link)

    return links


def fetch_title(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        return soup.title.string.strip() if soup.title else "NO TITLE"
    except Exception as e:
        return f"ERROR: {e}"


if __name__ == "__main__":
    query = "閉店 店舗名 公式"
    links = google_search(query)

    print("Google results:")
    for link in links[:5]:
        title = fetch_title(link)
        print(f"- {title}")
        print(f"  {link}")
