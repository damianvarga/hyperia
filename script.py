import requests
import json
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


URL = "https://www.prospektmaschine.de/brochure-geo/get-brochures-for-template/"

PARAMS = {
    "type": "category",
    "categoryId": 11,      # Hypermarkety / Supermarkety
}

resp = requests.get(URL, params=PARAMS, timeout=15)
resp.raise_for_status()
data = resp.json()

result = []
seen = set()
for b in data:
    shop_id = b.get("shopId") or b.get("retailerId")
    shop_name = b.get("shopName") or b.get("retailerName")
    brochure_id = b.get("brochureId")

    start_end_text = b.get("startEndText")

    valid_from = None
    valid_to = None

    if start_end_text:
        start_str, end_str = start_end_text.split(" - ")

        valid_from = datetime.strptime(start_str, "%d.%m.%Y").strftime("%Y-%m-%d")
        valid_to = datetime.strptime(end_str, "%d.%m.%Y").strftime("%Y-%m-%d")
        
    item = {
        "title": b.get("title") or b.get("brochureName"),
        "thumbnail": b.get("brochureImageSrc"),
        "shop_name": shop_name,
        "valid_from": valid_from,
        "valid_to": valid_to,
        "parsed_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    result.append(item)

with open("supermarkety_letaky.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Uložených letákov: {len(result)}")


