import requests
from bs4 import BeautifulSoup
import csv

url = "https://realpython.github.io/fake-jobs/"
reponse = requests.get(url)

if reponse.status_code == 200:
    soup = BeautifulSoup(reponse.text, "html.parser")

    job_card = soup.find_all("div", class_="card-content")

    with open("mock3.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Job Title", "Company", "Location", "Job Link"])

        for card in job_card:

            title_tag = card.find("h2", class_="title is-5")
            if not title_tag:
                continue
            title = title_tag.get_text(strip=True)
            if "python" not in title.lower():
                continue

            company_tag = card.find("h3", class_="subtitle is-6 company")
            company = company_tag.get_text(strip=True) if company_tag else ""

            location_tag = card.find("p", class_="location")
            location = location_tag.get_text(strip=True) if location_tag else ""

            footer = card.find("footer", class_="card-footer")
            apply_tag = footer.find_all("a")[1]
            job_url = apply_tag["href"]

            writer.writerow([title, company, location, job_url])

    print("Jobs scraped successfully")

else:
    print("Operation Failed")





    
