from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

# 検索ワード（あとで増やせる）
query = "TSUTAYA 閉店"
url = f"https://x.com/search?q={query}&f=live"

driver.get(url)
time.sleep(10)  # 読み込み待ち

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)

links = set()
elements = driver.find_elements(By.XPATH, "//a[contains(@href,'/status/')]")

for e in elements:
    links.add(e.get_attribute("href"))

driver.quit()

print("PAGE TITLE:", driver.title)

print("X results:")
for link in list(links)[:10]:
    print(link)
