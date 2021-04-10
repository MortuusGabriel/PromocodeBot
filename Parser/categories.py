import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

URL = 'https://promokod.pikabu.ru/category'
HEADERS = {
    'User-Agent': UserAgent().chrome
}


def get_html(url, params=None):
    session = requests.Session()
    session.headers = HEADERS
    full_page = session.get(url)
    full_page.encoding = 'utf8'
    return full_page


def get_categories():
    soup = BeautifulSoup(get_html(URL).text, 'html.parser')
    block = soup.find('div', class_='row')
    cards = block.find_all('a')
    categories = []
    for card in cards:
        categories.append({
            'name': card.get('title'),
            'href': card.get('href')
        })
    return categories


def get_category_shops(url):
    soup = BeautifulSoup(get_html(url).text, 'html.parser')
    block = soup.find('div', class_='categories-list')
    items = block.find_all('a')
    shops = []
    for item in items:
        shops.append({
            'name': item.get_text(),
            'href': item.get('href')
        })
    return shops


if __name__ == '__main__':
    print(get_category_shops('https://promokod.pikabu.ru/category/apteki-i-zdorove'))
