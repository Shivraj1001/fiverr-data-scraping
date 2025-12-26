import requests
from bs4 import BeautifulSoup
import csv
import time
from urllib.parse import urljoin

def scrape_page(url, writer, seen_quotes):
    try:
        response = requests.get(
            url, headers={"User-Agent":"Mozilla/5.0"}, timeout=10
        )
        if response.status_code != 200:
            return False
    except requests.exceptions.RequestException:
        return False
    
    soup = BeautifulSoup(response.text, "html.parser")
    quotes = soup.find_all("div", class_="quote")

    if not quotes:
        return None

    for quote in quotes:
        statement = quote.find("span", class_="text")
        author = quote.find("small", class_="author")
        tags = quote.find_all("a", class_="tag")

        writer.writerow([
            statement.get_text(strip=True) if statement else "",
            author.get_text(strip=True) if author else "",
            ", ".join(tag.get_text(strip=True) for tag in tags)
        ])

    next_li = soup.find("li", class_="next")
    if next_li:
        next_href = next_li.find("a")["href"]
        return urljoin(url, next_href)

    return None

with open("adv5.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Quotes", "Author", "Tags"])

    seen_quotes = set()

    page = 1
    url = "https://quotes.toscrape.com/page/1/"

    while url:
        print(f"---Scraping page {page}---")
        url = scrape_page(url, writer, seen_quotes)

        page += 1
        time.sleep(1)
print("Scrapping completed successfully")
            
