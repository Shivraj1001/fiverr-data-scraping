import requests
from bs4 import BeautifulSoup
import csv

def scrape_page(url, writer):
    headers = {"User-Agent":"Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return False
    except requests.exceptions.RequestException:
        return False
    
    soup = BeautifulSoup(response.text, "html.parser")
    quotes = soup.find_all("div", class_="quote")

    for quote in quotes:
        statement_tag = quote.find("span", class_="text")
        statement = statement_tag.get_text(strip=True) if statement_tag else ""
        if statement in seen_quotes:
            continue
        seen_quotes.add(statement)

        author_tag = quote.find("small", class_="author")
        author = author_tag.get_text(strip=True) if author_tag else ""

        tags_tag = quote.find_all("a", class_="tag")
        tags = ", ".join(tag.get_text(strip=True) for tag in tags_tag)

        writer.writerow([statement, author, tags])
    return True

with open("adv1.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Quotes", "Author", "Tags"])

    seen_quotes = set()

    base_url = "https://quotes.toscrape.com/page/{}/"

    for page in range(1, 100):
        url = base_url.format(page)
        success = scrape_page(url, writer)

        if not success:
            break
print("Multiple pages scraped successfully")