from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup

HEADERS = {
    'Referer': 'https://promokodi.net/store/?__cf_chl_captcha_tk__=308b9e229c42002ded46481f646ef74e537a07ad-1612817143-0-Ae6MJrNPpEkB2TJqBZ3Ch1ZpqgclAiJ2yla0EZyjU6tiRqhOH5XACE_cpgj7JVkV2JQOG7GtxFPnQ94xCGXCpLn-N0wbjRFZHC5e6_P-KMRZxsjdbvP6U07zNYqav7wKEEigwJ5UcU9Ea4b4mKDkvRMZeZsK-dcV1dGbXyxG6Z6irejbh4O4hgGqryMN7LSICQ_mf5jUgNp6f0KizF1X01gN6p4IfYtBLkb_Q6QI0DXUnNOaND_9mXeODLErdhBr8W6LFy2RJDAsVXv1P_xNSdvOHk4AFw9sBrmM6LVS018qQR11z8kDD7xW1iRwnprwM6Az1f7c8Xc5WohvUSeFquLDZJjdis_NUbwzBzCK3-ayalHXb4B3fO8IYkk5uUYNhmDEVaBwFjLgoLGO59IpHXEJAnTJSS4g_ETI69TL6v7pf41QTpxfA1Qwhw9lL_vTw4gVzAxmpVde2UasU5MH8r_ZQERQVlCVew7mSN6k39oxakQGRWaE9_buOQ_tkiy_BGWjGTUQY5UBg9Hda_UCcWSCF_3dFPFn7yWMBrPKTVFzqEXBCTvfd5YmmHHNPrnFmjQ7MI77-2ftKpc4pGddrJ0',
    'User-Agent': UserAgent().chrome
}


def interceptor(request):
    del request.headers['Referer']
    request.headers['Referer'] = HEADERS['Referer']


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
