"""
Utilities for working with data translations (news, products, etc.)
"""
from typing import Any, Dict, List, Optional
from models.news import News
from models.product import Product


def get_translated_news(news: News, lang: str = 'ru') -> Dict[str, Any]:
    return {
        'id': news.id,
        'title': news.get_title(lang),
        'content': news.get_content(lang),
        'category': news.get_category(lang),
        'author': news.get_author(lang),
        'created_at': news.created_at,
        'image': news.image,
        'is_published': news.is_published,
        'views_count': news.views_count
    }


def get_translated_product(product: Product, lang: str = 'ru') -> Dict[str, Any]:
    return {
        'id': product.id,
        'name': product.get_name(lang),
        'description': product.get_description(lang),
        'price': product.price,
        'category': product.get_category(lang),
        'image': product.image,
        'stock': product.stock,
        'is_available': product.is_available
    }


def get_translated_news_list(news_list: List[News], lang: str = 'ru') -> List[Dict[str, Any]]:
    return [get_translated_news(news, lang) for news in news_list]


def get_translated_products_list(products_list: List[Product], lang: str = 'ru') -> List[Dict[str, Any]]:
    return [get_translated_product(product, lang) for product in products_list]
