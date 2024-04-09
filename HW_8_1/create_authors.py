import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

# Функція для отримання додаткової інформації про авторів
def scrape_author_info(author_url):
    response = requests.get(author_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Отримання імені автора
    fullname_tag = soup.find('h3', class_='author-title')
    fullname = fullname_tag.text.strip()
    
    # Отримання інформації про дату народження та місце народження
    born_date_tag = soup.find('span', class_='author-born-date')
    born_date = born_date_tag.text.strip() if born_date_tag else ''
    
    born_location_tag = soup.find('span', class_='author-born-location')
    born_location = born_location_tag.text.strip() if born_location_tag else ''
    
    # Отримання опису автора
    description_tag = soup.find('div', class_='author-description')
    description = description_tag.text.strip() if description_tag else ''
    
    return {'fullname': fullname, 'born_date': born_date, 'born_location': born_location, 'description': description}

# Функція для отримання посилання на наступну сторінку
def get_next_page_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    next_page = soup.find('li', class_='next')
    if next_page:
        next_page_url = urljoin(url, next_page.find('a')['href'])
        return next_page_url
    else:
        return None

def main():
    base_url = 'http://quotes.toscrape.com'
    current_url = base_url
    authors_info = []

    # Скрапінг інформації про авторів
    while current_url:
        response = requests.get(current_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for quote_tag in soup.find_all('div', class_='quote'):
            author_url = quote_tag.find('small', class_='author').find_next('a')['href']
            author_url = urljoin(base_url, author_url)
            author_info = scrape_author_info(author_url)
            authors_info.append(author_info)
        current_url = get_next_page_url(current_url)

    # Зберігання інформації про авторів у файл authors.json
    with open('authors.json', 'w', encoding='utf-8') as f:
        json.dump(authors_info, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()
