from flask import Flask
import requests
from bs4 import BeautifulSoup
import logging


headers_pc = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13.2.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36", }

target_url = 'https://auctions.yahoo.co.jp/search/search/%E3%82%A2%E3%83%BC%E3%82%AF%E3%83%86%E3%83%AA%E3%82%AF%E3%82%B9%20%E3%83%AA%E3%83%A5%E3%83%83%E3%82%AF/0/?rs=3'

def get_bid_num(product: BeautifulSoup):
    bid_num = int(product.find('span', {'class':'Product__bid'}).text)
    return bid_num

def get_items_content(product: BeautifulSoup):
    img_src = product.find('img').get('src')
    title = product.find('h3').text
    item_dic = {
        'title': title,
        'img_src': img_src
    }
    return item_dic

def test():
    res = requests.get(target_url)
    html = res.text

    soup = BeautifulSoup(html, "html.parser")
    products_list = soup.find('ul', {'class' : 'Products__items'}).find_all('li', {'class': 'Product'})
    # len = len(products_list)
    # title = soup.title.text
    with_bid = [prod for prod in products_list if get_bid_num(prod) > 0]
    # 入札ありが0件の時
    if not len(with_bid):
        return

    img_src_list = [get_items_content(src) for src in with_bid]
    return img_src_list
    # print(f'img_src:{img_src_list}')

    # app.logger.debug('This is a debug message')