"""
SDU SuperApp - Main Application File
Web platform for SDU students and teachers
Course: CSS 217 - Software Architecture and Design Patterns
Year: 2025
"""

from flask import Flask, render_template, session, request
from config import config
from utils.i18n import get_translation, get_language_name, SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE

from controllers.main_controller import main_bp
from controllers.teacher_controller import teacher_bp
from controllers.review_controller import review_bp
from controllers.room_controller import room_bp
from controllers.news_controller import news_bp
from controllers.shop_controller import shop_bp
from controllers.admin_controller import admin_bp
from controllers.language_controller import language_bp

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    app.register_blueprint(main_bp)
    app.register_blueprint(teacher_bp, url_prefix='/teachers')
    app.register_blueprint(review_bp, url_prefix='/reviews')
    app.register_blueprint(room_bp, url_prefix='/rooms')
    app.register_blueprint(news_bp, url_prefix='/news')
    app.register_blueprint(shop_bp, url_prefix='/shop')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(language_bp, url_prefix='/lang')
    
    #for language detection
    @app.before_request
    def set_language():
        if 'language' not in session:
            accept_language = request.accept_languages.best_match(SUPPORTED_LANGUAGES)
            session['language'] = accept_language if accept_language else DEFAULT_LANGUAGE
    

    #for language translation
    @app.context_processor
    def inject_i18n():
        current_lang = session.get('language', DEFAULT_LANGUAGE)
        
        def t(key, **kwargs):
            return get_translation(key, current_lang, **kwargs)
        
        return {
            't': t,
            'current_language': current_lang,
            'supported_languages': SUPPORTED_LANGUAGES,
            'get_language_name': get_language_name
        }


    #for 404 error
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app


if __name__ == '__main__':
    app = create_app('development')

    app.run(host='0.0.0.0', port=5001, debug=True)


