from flask import Blueprint, render_template, request, redirect, url_for
from scraping_yahoo import test
from scrape_method.arcteryx import arcteryx_offical, sunday_mountain_shop
from scrape_method.get_money import GetDataBeautySalon, my_test
from scrape_method.dental import run, get_page_count, abc, save_to_csv
from tqdm import tqdm

product_bp = Blueprint('product', __name__)

@product_bp.route('/test', methods=['GET'])
def get_data():
    print(__name__)
    # img_src_list = test()
    arcteryx = arcteryx_offical()
    sunsay_shop = sunday_mountain_shop()
    return render_template('saerce.html', arcteryx=arcteryx, sunsay_shop=sunsay_shop)


@product_bp.route('/get_salon', methods=['GET'])
def get_salon():
    # get_salon_info = GetDataBeautySalon()
    # res = get_salon_info.run()
    data = my_test()

    # return render_template('salon.html')
    return render_template('salon.html', local_list=data)



# ! データ取得するページ数の取得とブラウザへの表示
@product_bp.route('/get_dental_urls', methods=['GET'])
def get_dental_urls():
    page_url = "https://haisha-yoyaku.jp/bun2sdental/list/category/catg/13/"
    page_count = get_page_count(page_url)
    url_list = [f"{page_url}?page={num}" for num in range(1, page_count +1)]
    # url_list = []

    return render_template('dental_page.html', url_list=url_list)

@product_bp.route('/get_dental/<int:page>', methods=['GET'])
def get_dental(page):
    page_url = f"https://haisha-yoyaku.jp/bun2sdental/list/category/catg/13/?page={page}"
    csv_data = run(page_url)
    save_to_csv(csv_data, page)
    data = []

    return render_template('dental.html', data_list=data)



























