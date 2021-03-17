from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from Parser.shops import get_link
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


HEADERS = {
    'Referer': 'https://promokodi.net/store/?__cf_chl_captcha_tk__=308b9e229c42002ded46481f646ef74e537a07ad-1612817143-0-Ae6MJrNPpEkB2TJqBZ3Ch1ZpqgclAiJ2yla0EZyjU6tiRqhOH5XACE_cpgj7JVkV2JQOG7GtxFPnQ94xCGXCpLn-N0wbjRFZHC5e6_P-KMRZxsjdbvP6U07zNYqav7wKEEigwJ5UcU9Ea4b4mKDkvRMZeZsK-dcV1dGbXyxG6Z6irejbh4O4hgGqryMN7LSICQ_mf5jUgNp6f0KizF1X01gN6p4IfYtBLkb_Q6QI0DXUnNOaND_9mXeODLErdhBr8W6LFy2RJDAsVXv1P_xNSdvOHk4AFw9sBrmM6LVS018qQR11z8kDD7xW1iRwnprwM6Az1f7c8Xc5WohvUSeFquLDZJjdis_NUbwzBzCK3-ayalHXb4B3fO8IYkk5uUYNhmDEVaBwFjLgoLGO59IpHXEJAnTJSS4g_ETI69TL6v7pf41QTpxfA1Qwhw9lL_vTw4gVzAxmpVde2UasU5MH8r_ZQERQVlCVew7mSN6k39oxakQGRWaE9_buOQ_tkiy_BGWjGTUQY5UBg9Hda_UCcWSCF_3dFPFn7yWMBrPKTVFzqEXBCTvfd5YmmHHNPrnFmjQ7MI77-2ftKpc4pGddrJ0',
    'User-Agent': UserAgent().chrome
}


def interceptor(request):
    del request.headers['Referer']
    request.headers['Referer'] = HEADERS['Referer']


def get_content(link):
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    # chrome_options.headless = True

    global driver
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
    driver.implicitly_wait(5)
    driver.request_interceptor = interceptor
    driver.get(link)
    sleep(3)
    items = driver.find_elements_by_class_name('is-cashback-store-offers-list-item-logocol')
    promos = []
    for item in items:
        promos.append({
            'title': item.find_element_by_tag_name('h3').text,
            'days remaining': item.find_element_by_class_name(
                'cashback-store-offers-list-item-active-to-container').text,
            'description': item.find_element_by_class_name('cashback-store-offers-list-item-description-content').text,
            'code_button': item.find_element_by_class_name('cashback-store-offers-list-item-btn-container')
        })

    return promos


def get_promo(button):
    window_before = driver.window_handles[0]
    button.click()
    link = driver.current_url
    window_after = driver.window_handles[1]
    if window_before != window_after:
        driver.switch_to.window(window_after)

    try:
        code = driver.find_element_by_id('_copied_promokode').get_attribute('value')
        description = driver.find_element_by_class_name('template-open-offer-description-container').text
    except Exception:
        code = driver.find_element_by_class_name('template-open-offer-no-code-container').text
        description = driver.find_element_by_class_name('template-open-offer-description-container').text
    finally:
        info = [code, description, link]

    driver.switch_to.window(window_before)
    driver.close()
    driver.switch_to.window(window_after)
    driver.find_element_by_class_name('close').click()
    return info


def parse(link):
    promos = get_content(link)
    print(get_promo(promos[0]['code_button']))


if __name__ == "__main__":
    parse()
