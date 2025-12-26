"""
News Controller
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from facade.sdu_facade import SDUFacade
from utils.data_i18n import get_translated_news, get_translated_news_list
from utils.i18n import DEFAULT_LANGUAGE, get_translation

news_bp = Blueprint('news', __name__)
facade = SDUFacade()


@news_bp.route('/')
def list_news():
    """News list."""
    category = request.args.get('category')
    search = request.args.get('search')
    lang = session.get('language', DEFAULT_LANGUAGE)

    if search:
        news = facade.search_news(search)
    elif category:
        news = facade.get_news_by_category(category)
    else:
        news = facade.get_news()

    # Translate news
    translated_news = get_translated_news_list(news, lang)

    categories = facade.get_news_categories()
    popular = facade.get_popular_news(5)
    translated_popular = get_translated_news_list(popular, lang)

    return render_template('news/list.html',
                          news=translated_news,
                          categories=categories,
                          popular_news=translated_popular,
                          current_category=category,
                          search_query=search)


@news_bp.route('/<news_id>')
def news_detail(news_id):
    """News detail page."""
    lang = session.get('language', DEFAULT_LANGUAGE)
    article = facade.get_news_article(news_id)

    if not article:
        return render_template('404.html'), 404

    # Translate news
    translated_article = get_translated_news(article, lang)

    popular = facade.get_popular_news(5)
    translated_popular = get_translated_news_list(popular, lang)

    return render_template('news/detail.html',
                          news=translated_article,
                          popular_news=translated_popular)


@news_bp.route('/subscribe', methods=['POST'])
def subscribe():
    """Subscribe to news."""
    email = request.form.get('email')
    name = request.form.get('name', 'Subscriber')
    lang = session.get('language', DEFAULT_LANGUAGE)

    if not email:
        flash(get_translation('news.subscribe_email_required', lang), 'error')
        return redirect(url_for('news.list_news'))

    if facade.subscribe_to_news(email, name, language=lang):
        flash(get_translation('news.subscribe_success', lang), 'success')
    else:
        flash(get_translation('news.subscribe_email_exists', lang), 'info')

    return redirect(url_for('news.list_news'))


@news_bp.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    """Unsubscribe from news."""
    email = request.form.get('email')

    if facade.unsubscribe_from_news(email):
        flash('You have been unsubscribed', 'success')
    else:
        flash('Email not found in subscriptions', 'error')

    return redirect(url_for('news.list_news'))


@news_bp.route('/unsubscribe/<subscriber_id>')
def unsubscribe_by_id(subscriber_id):
    """Unsubscribe from news by ID (for link from email)."""
    from repository.subscriber_repository import SubscriberRepository
    
    repo = SubscriberRepository()
    subscriber = repo.get_by_id(subscriber_id)
    
    if subscriber:
        repo.deactivate(subscriber_id)
        flash('You have been unsubscribed successfully', 'success')
    else:
        flash('Subscription not found', 'error')
    
    return redirect(url_for('news.list_news'))

