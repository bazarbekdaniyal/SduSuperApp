"""
Language switch controller
"""
from flask import Blueprint, session, redirect, request, url_for
from utils.i18n import SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE

language_bp = Blueprint('language', __name__)


@language_bp.route('/set/<lang>')
def set_language(lang):
    """
    Sets language in session and redirects back
    
    Args:
        lang: Language code (ru, en, kz)
    """
    if lang in SUPPORTED_LANGUAGES:
        session['language'] = lang
    
    # Redirect to previous page or home
    next_page = request.referrer or url_for('main.index')
    return redirect(next_page)
