"""
Internationalization System
Supported languages: ru, en, kz
"""
import json
import os

TRANSLATIONS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'translations')

SUPPORTED_LANGUAGES = ['ru', 'en', 'kz']
DEFAULT_LANGUAGE = 'ru'


def load_translations(lang):
    if lang not in SUPPORTED_LANGUAGES:
        lang = DEFAULT_LANGUAGE
    
    file_path = os.path.join(TRANSLATIONS_DIR, f'{lang}.json')
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def get_translation(key, lang=DEFAULT_LANGUAGE, **kwargs):
    if not key:
        return ''
    
    translations = load_translations(lang)
    
    if not translations:
        return key

    keys = key.split('.')
    value = translations
    
    try:
        for k in keys:
            if not isinstance(value, dict):
                return key
            value = value[k]
        
        if kwargs and isinstance(value, str):
            return value.format(**kwargs)
        if isinstance(value, (str, int, float)):
            return str(value)
        
        return key
    except (KeyError, TypeError, AttributeError):
        return key


def get_language_name(lang_code):
    names = {
        'ru': 'Русский',
        'en': 'English',
        'kz': 'Қазақша'
    }
    return names.get(lang_code, lang_code)


def get_days_of_week(lang=DEFAULT_LANGUAGE):
    translations = load_translations(lang)
    schedule = translations.get('schedule', {})
    
    return {
        1: schedule.get('monday', 'Monday'),
        2: schedule.get('tuesday', 'Tuesday'),
        3: schedule.get('wednesday', 'Wednesday'),
        4: schedule.get('thursday', 'Thursday'),
        5: schedule.get('friday', 'Friday'),
        6: schedule.get('saturday', 'Saturday')
    }
