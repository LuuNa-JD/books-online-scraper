import requests
from bs4 import BeautifulSoup
import csv

url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extraction des informations nécessaires
product_page_url = url
upc = soup.find('th', text='UPC').find_next_sibling('td').text
title = soup.find('h1').text
price_including_tax = soup.find('th', text='Price (incl. tax)').find_next_sibling('td').text
price_excluding_tax = soup.find('th', text='Price (excl. tax)').find_next_sibling('td').text
number_available = soup.find('th', text='Availability').find_next_sibling('td').text
product_description = soup.find('h2', text='Product Description').find_next('p').text.strip()
review_rating = soup.find('p', class_='star-rating')['class'][1]
category = soup.find('ul', class_='breadcrumb').find_all('li')[2].text.strip()
image_url = soup.find('img')['src'].replace('../..', 'https://books.toscrape.com')


# Création du fichier CSV

with open('book_data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['product_page_url', 'universal_product_code', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url'])
    writer.writerow([product_page_url, upc, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url])
