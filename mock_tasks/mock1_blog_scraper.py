import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.zyte.com/blog/"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    blogs = soup.find_all("div", class_="CardBlogList_cardContainer__LSYMV")

    with open("mock1.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Article", "Author", "Publish Date"])

        for blog in blogs:
            article = blog.find("h2", class_="CardBlogList_title__ZjVlV mt-16").text

            author = blog.find("a", class_="CardBlogList_link__ZiiuJ").text
            
            published_date = blog.find("span", class_="CardBlogList_date__Fegia heading-extra-extra-small").text
            
            writer.writerow([article, author, published_date])

    print("Saved successfully")

else:
    print("Operation Failed")