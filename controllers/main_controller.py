"""
Main controller - home page
"""
from flask import Blueprint, render_template, session
from facade.sdu_facade import SDUFacade
from utils.data_i18n import get_translated_news_list, get_translated_products_list
from utils.i18n import DEFAULT_LANGUAGE

main_bp = Blueprint('main', __name__)
facade = SDUFacade()


@main_bp.route('/')
def index():
    """Home page."""
    lang = session.get('language', DEFAULT_LANGUAGE)
    data = facade.get_home_page_data()
    
    # Translate news and products
    translated_news = get_translated_news_list(data['latest_news'], lang)
    translated_products = get_translated_products_list(data['products'], lang)
    
    return render_template('index.html',
                          top_teachers=data['top_teachers'],
                          latest_news=translated_news,
                          products=translated_products)


@main_bp.route('/about')
def about():
    """About page."""
    return render_template('about.html')



