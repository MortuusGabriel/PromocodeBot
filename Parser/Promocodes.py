from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': UserAgent().chrome
}


def get_html(url, params=None):
    session = requests.Session()
    session.headers = HEADERS
    full_page = session.get(url)
    full_page.encoding = 'utf8'

    return full_page


def get_content(url):
    html = get_html(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    tovars = soup.find('div', class_='tovars')
    items = tovars.find_all('div', class_='item-tovars')
    promos = []
    for item in items:
        description = item.find('div', class_='tovav-content')
        button = item.find('div', class_='open-tovar')
        promos.append({
            'title': description.find('a', class_='click-coupon', href='#').get_text().replace('\n', '').replace('\t',
                                                                                                                 ''),
            'description': description.find_all('p')[1].get_text().replace(str('\xa0'), ' '),
            'promo': button.find('a').get('data-code'),
            'link': button.find('a').get('href')
        })
    promos.append(url)
    return promos


if __name__ == "__main__":
    print(get_content('https://promokod.pikabu.ru/shops/asos'))
