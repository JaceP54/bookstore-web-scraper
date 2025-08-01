import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

url = "https://books.toscrape.com"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

books = soup.find_all("article", class_="product_pod")

data = []

for i, book in enumerate(books, start=1):
    h3_tag = book.find("h3")
    a_tag = h3_tag.find("a") if h3_tag else None
    price_tag = book.find("p", class_="price_color")

    if a_tag and a_tag.has_attr("title"):
        title = a_tag["title"]
        price = price_tag.text.strip() if price_tag else "N/A"
        print(f"{i}. {title} - {price}")
        data.append([title, price])
    else:
        print(f"{i}. Title not found.")



with open('output_plain.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Price"])  # Write the header row
    writer.writerows(data)

df = pd.DataFrame(data, columns=["Title", "Price"])
df.to_csv("output_pandas.xlsx", index=False)
