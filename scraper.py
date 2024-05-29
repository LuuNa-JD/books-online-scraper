import requests
from bs4 import BeautifulSoup
import csv

# Récupération des URLs des catégories
def get_book_urls(category_url):
    book_urls = []
    while category_url:
        response = requests.get(category_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        book_links = soup.select('h3 a')
        for link in book_links:
            book_urls.append(link['href'].replace('../../..', 'https://books.toscrape.com/catalogue'))

        next_button = soup.find('li', class_='next')
        if next_button:
            next_page = next_button.find('a')['href']
            category_url = category_url.rsplit('/', 1)[0] + '/' + next_page
        else:
            category_url = None
    return book_urls

# Récupération des données d'un livre
def extract_book_data(book_url):
    response = requests.get(book_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    data = {
        'product_page_url': book_url,
        'upc': soup.find('th', string='UPC').find_next_sibling('td').text,
        'title': soup.find('h1').text,
        'price_including_tax': soup.find('th', string='Price (incl. tax)').find_next_sibling('td').text,
        'price_excluding_tax': soup.find('th', string='Price (excl. tax)').find_next_sibling('td').text,
        'number_available': soup.find('th', string='Availability').find_next_sibling('td').text,
        'product_description': soup.find('h2', string='Product Description').find_next('p').text.strip(),
        'review_rating': soup.find('p', class_='star-rating')['class'][1],
        'category': soup.find('ul', class_='breadcrumb').find_all('li')[2].text.strip(),
        'image_url': soup.find('img')['src'].replace('../..', 'https://books.toscrape.com')
    }
    return data

# Récupération des données d'une catégorie
def scrape_category(category_url):
    book_urls = get_book_urls(category_url)
    all_books_data = []

    for book_url in book_urls:
        book_data = extract_book_data(book_url)
        all_books_data.append(book_data)

    return all_books_data

# Sauvegarde des données dans un fichier CSV
def save_books_data_to_csv(books_data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['product_page_url', 'universal_product_code', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url'])
        for book_data in books_data:
            writer.writerow(book_data.values())

# URL de la catégorie à scraper
category_url = input('Entrez l\'URL de la catégorie à scraper: ')
books_data = scrape_category(category_url)
save_books_data_to_csv(books_data, 'one_category_books.csv')
