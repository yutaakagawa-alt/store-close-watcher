from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

query = "TSUTAYA 閉店"
url = f"https://www.google.com/search?q={query}"

driver.get(url)
time.sleep(10)

links = set()
elements = driver.find_elements(By.XPATH, "//a")

for e in elements:
    href = e.get_attribute("href")
    if href and "http" in href and "google" not in href:
        links.add(href)
        
print("HTML LENGTH:", len(driver.page_source))
print(driver.page_source[:500])
print("PAGE TITLE:", driver.title)

driver.quit()

print("PAGE TITLE:", driver.title)

print("Google results:")
for link in list(links)[:10]:
    print(link)
