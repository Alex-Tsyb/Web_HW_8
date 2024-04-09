from bs4 import BeautifulSoup
import json
import requests
from urllib.parse import urljoin

def scrape_quotes(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes = []

    # Знаходимо всі елементи цитат
    quote_tags = soup.find_all('div', class_='quote')
    for quote_tag in quote_tags:
        text = quote_tag.find('span', class_='text').text.strip()
        author = quote_tag.find('small', class_='author').text.strip()
        tags = [tag.text for tag in quote_tag.find_all('a', class_='tag')]
        
        quote_info = {'tags': tags, 'author': author, 'quote': text}
        quotes.append(quote_info)

    return quotes

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
    quotes = []

    # Скрапінг цитат
    while current_url:
        quotes += scrape_quotes(current_url)
        current_url = get_next_page_url(current_url)

    # Зберігання цитат у файл qoutes.json
    with open('qoutes.json', 'w', encoding='utf-8') as f:
        json.dump(quotes, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()
