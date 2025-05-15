# scraper.py
import requests
from bs4 import BeautifulSoup
import time

def fetch_page(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'lxml')

def parse_products(soup, search_term):
    products = soup.find_all('div', class_='astra-shop-summary-wrap')
    results = []
    for product in products:
        beer_name_tag = product.find('h2', class_='woocommerce-loop-product__title')
        price_tag = product.find('span', class_='woocommerce-Price-amount amount')

        if beer_name_tag and price_tag:
            beer_name = beer_name_tag.text.strip()
            price = price_tag.text.strip()

            if search_term in beer_name.lower():
                results.append((beer_name, price))

    return results

def scrape_beers(search_term, base_url='https://www.bottleworks.com/shop/'):
    page = 1
    all_results = []

    while True:
        url = f'{base_url}page/{page}/'
        soup = fetch_page(url)
        if not soup:
            break

        results = parse_products(soup, search_term)
        if results:
            all_results.extend(results)

        next_page_tag = soup.find('a', class_='next page-numbers')
        if next_page_tag:
            page += 1
            time.sleep(1)
        else:
            break

    return all_results
