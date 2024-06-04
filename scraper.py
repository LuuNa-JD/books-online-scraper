import requests
from bs4 import BeautifulSoup
import csv
import os


# Extraction des URLs des catégories
def get_category_urls(base_url):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    category_links = soup.select('div.side_categories ul.nav-list li ul li a')
    category_urls = {link.text.strip(): base_url + link['href'] for link in category_links}
    return category_urls

# Extraction des URLs des livres dans une catégorie
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

# Extraction des données deslivre
def get_book_data(book_url):
    response = requests.get(book_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    image_url = soup.find('img')['src'].replace('../..', 'https://books.toscrape.com') if soup.find('img') else None

    data = {
        'product_page_url': book_url if book_url else None,
        'upc': soup.find('th', string='UPC').find_next_sibling('td').text if soup.find('th', string='UPC') else None,
        'title': soup.find('h1').text if soup.find('h1') else None,
        'price_including_tax': soup.find('th', string='Price (incl. tax)').find_next_sibling('td').text if soup.find('th', string='Price (incl. tax') else None,
        'price_excluding_tax': soup.find('th', string='Price (excl. tax)').find_next_sibling('td').text if soup.find('th', string='Price (excl. tax)') else None,
        'number_available': soup.find('th', string='Availability').find_next_sibling('td').text if soup.find('th', string='Availability') else None,
        'product_description': soup.find('h2', string='Product Description').find_next('p').text.strip() if soup.find('h2', string='Product Description') else None,
        'review_rating': soup.find('p', class_='star-rating')['class'][1] if soup.find('p', class_='star-rating') else None,
        'category': soup.find('ul', class_='breadcrumb').find_all('li')[2].text.strip() if soup.find('ul', class_='breadcrumb') else None,
        'image_url': image_url
    }
    return data

# Téléchargement d'une image
def download_image(image_url, save_path):
    response = requests.get(image_url)
    with open(save_path, 'wb') as file:
        file.write(response.content)


# Récupération des données de tous les livres d'une catégorie
def scrape_category(category_url, category_name):
    book_urls = get_book_urls(category_url)
    all_books_data = []

    image_dir = f'images/{category_name}'
    os.makedirs(image_dir, exist_ok=True)

    for book_url in book_urls:
        book_data = get_book_data(book_url)
        all_books_data.append(book_data)
        if book_data['image_url']:
            image_filename = os.path.join(image_dir, f"{book_data['title'].replace(' ', '_').replace('/', '_')}.jpg")
            download_image(book_data['image_url'], image_filename)

    return all_books_data

# Sauvegarde des données de livre dans un fichier CSV
def save_books_data_to_csv(books_data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['product_page_url', 'universal_product_code', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url'])
        for book_data in books_data:
            writer.writerow(book_data.values())

# Récupération des données de tous les livres de toutes les catégorie
def scrape_all_categories(base_url):
    category_urls = get_category_urls(base_url)
    for category, url in category_urls.items():
        print(f'Scraping de la categorie: {category}')
        books_data = scrape_category(url, category.replace(" ", "_").lower())
        filename = f'{category.replace(" ", "_").lower()}_books.csv'
        save_books_data_to_csv(books_data, filename)
        print(f'Sauvegarde de {len(books_data)} livres dans le fichier : {filename}')

# URL de la catégorie à scraper
base_url = "https://books.toscrape.com/"
scrape_all_categories(base_url)
