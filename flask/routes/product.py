from flask import Blueprint, render_template, request, redirect, url_for
from scraping_yahoo import test

product_bp = Blueprint('product', __name__)

@product_bp.route('/test', methods=['GET'])
def get_data():
    print(__name__)
    img_src_list = test()
    return render_template('saerce.html', data=img_src_list)