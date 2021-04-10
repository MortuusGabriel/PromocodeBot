import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import process
from fake_useragent import UserAgent

URL = 'https://promokod.pikabu.ru/shops'
HEADERS = {
    'User-Agent': UserAgent().chrome
}


def get_html(url, params=None):
    session = requests.Session()
    session.headers = HEADERS
    full_page = session.get(url)
    full_page.encoding = 'utf8'
    return full_page


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    cards = soup.find_all('div', class_='topshop-home')
    shops = []
    for card in cards:
        items = card.find_all('li')
        for item in items:
            shops.append({
                'name': item.find('a').get('title'),
                'href': item.find('a').get('href')
            })

    return shops


def find(name):
    html = get_html(URL)
    shops = get_content(html.text)
    result = process.extract(name, shops, limit=3)
    return result


if __name__ == '__main__':
    find(input())
