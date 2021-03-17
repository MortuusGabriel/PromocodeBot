import requests
import csv
import cfscrape
from bs4 import BeautifulSoup
from fuzzywuzzy import process

URL = 'https://promokodi.net/store/'
HEADERS = {
    'Referer': 'https://promokodi.net/store/?__cf_chl_captcha_tk__=308b9e229c42002ded46481f646ef74e537a07ad-1612817143-0-Ae6MJrNPpEkB2TJqBZ3Ch1ZpqgclAiJ2yla0EZyjU6tiRqhOH5XACE_cpgj7JVkV2JQOG7GtxFPnQ94xCGXCpLn-N0wbjRFZHC5e6_P-KMRZxsjdbvP6U07zNYqav7wKEEigwJ5UcU9Ea4b4mKDkvRMZeZsK-dcV1dGbXyxG6Z6irejbh4O4hgGqryMN7LSICQ_mf5jUgNp6f0KizF1X01gN6p4IfYtBLkb_Q6QI0DXUnNOaND_9mXeODLErdhBr8W6LFy2RJDAsVXv1P_xNSdvOHk4AFw9sBrmM6LVS018qQR11z8kDD7xW1iRwnprwM6Az1f7c8Xc5WohvUSeFquLDZJjdis_NUbwzBzCK3-ayalHXb4B3fO8IYkk5uUYNhmDEVaBwFjLgoLGO59IpHXEJAnTJSS4g_ETI69TL6v7pf41QTpxfA1Qwhw9lL_vTw4gVzAxmpVde2UasU5MH8r_ZQERQVlCVew7mSN6k39oxakQGRWaE9_buOQ_tkiy_BGWjGTUQY5UBg9Hda_UCcWSCF_3dFPFn7yWMBrPKTVFzqEXBCTvfd5YmmHHNPrnFmjQ7MI77-2ftKpc4pGddrJ0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 YaBrowser/20.12.3.140 Yowser/2.5 Safari/537.36',
}
FILE = 'shops.csv'


def get_html(url, params=None):
    session = requests.Session()
    session.headers = HEADERS
    full_page = session.get(url)
    full_page.encoding = 'utf8'

    return full_page


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('li', class_='cashback-stores-list-item')
    shops = []
    for item in items:
        shops.append({
            'name': item.find('a').get_text(),
            'href': item.find('a').get('href')
        })

    return (shops)


def get_link(search):
    return('https://promokodi.net' + search)


def find(name):
    html = get_html(URL)
    shops = get_content(html.text)
    result = process.extract(name, shops, limit=3)
    return result


if __name__ == '__main__':
    get_link()