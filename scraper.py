import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/"

response = requests.get(url)

if response.ok:
    soup = BeautifulSoup(response.text, "html.parser")
    books_title = soup.find_all("h3").text

    print(books_title)
