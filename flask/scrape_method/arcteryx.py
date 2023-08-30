from flask import Flask
import requests
from bs4 import BeautifulSoup

headers_pc = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13.2.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36", }


def arcteryx_offical():
  target_url = 'https://arcteryx.jp/products/granville-25-backpack?variant=46547246153959'

  res = requests.get(target_url)
  html = res.text
  supe = BeautifulSoup(html, "html.parser")

  have_stock = supe.find("div", {'id':'variant-inventory'}).find("span").text.strip()
  stock_bool = have_stock != "在庫なし"
  arcteryx = {"url": target_url, "stock": have_stock, "stock_bool": stock_bool}
  return arcteryx


def sunday_mountain_shop():
  target_url = "https://www.sundaymountain.jp/c/brand/arcteryx/a31425"

  res = requests.get(target_url)
  html = res.text
  supe = BeautifulSoup(html, "html.parser")

  li_el = supe.find("ul", {"class": "fs-c-variationList__item__cart"}).find_all("li")
  black_color_item_el = [li for li in li_el if li.find("span", {"class": "fs-c-variationCart__variationName__name"}).text.strip() == "ブラック"]
  stock = black_color_item_el[0].find("span", {"class": "fs-c-variationCart__variationName__stock--outOfStock"}).text.strip()
  stock_bool = stock != "在庫切れ"
  result = {"url": target_url, "stock": stock, "stock_bool": stock_bool}
  return result