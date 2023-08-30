from flask import Blueprint, render_template, request, redirect, url_for
from scraping_yahoo import test
from scrape_method.arcteryx import arcteryx_offical, sunday_mountain_shop
from scrape_method.get_money import get_data_beauty_salon

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
    # salon_urls_list = get_data_beauty_salon()

    return render_template('salon.html')
    # return render_template('salon.html', local_list=salon_urls_list)