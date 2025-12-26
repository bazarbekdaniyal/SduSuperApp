"""
News Automatic Translation Service
"""
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class TranslationService:
    """
    Service for automatic text translation.
    Uses deep-translator library for translation.
    """

    def __init__(self):
        self._translator = None
        self._init_translator()

    def _init_translator(self):
        """Initializes translator"""
        try:
            from deep_translator import GoogleTranslator
            self._translator = GoogleTranslator
            logger.info("Translation service initialized successfully")
            print("✓ Translation service initialized successfully")
        except ImportError:
            logger.warning("deep-translator not installed. Translations will be disabled.")
            print("⚠️  deep-translator library is not installed!")
            print("   Install it using: pip install deep-translator")
            self._translator = None

    def translate_text(self, text: str, source_lang: str = 'ru', target_lang: str = 'en') -> Optional[str]:
        """
        Translates text from one language to another.
        
        Args:
            text: Text to translate
            source_lang: Source language (ru, en, kz)
            target_lang: Target language (ru, en, kz)
            
        Returns:
            Translated text or None if error occurs
        """
        if not text or not text.strip():
            return text

        if source_lang == target_lang:
            return text

        if not self._translator:
            logger.warning("Translator not available")
            return text

        try:
            # Language mapping for Google Translator
            lang_map = {
                'ru': 'ru',
                'en': 'en',
                'kz': 'kk'  # Kazakh language in Google Translate
            }

            source = lang_map.get(source_lang, source_lang)
            target = lang_map.get(target_lang, target_lang)

            translator = self._translator(source=source, target=target)
            translated = translator.translate(text)
            
            logger.info(f"Translated text from {source_lang} to {target_lang}")
            return translated

        except Exception as e:
            logger.error(f"Translation error: {str(e)}")
            return text

    def translate_news(self, title: str, content: str, category: str, author: str, 
                      source_lang: str = 'ru') -> Dict[str, Dict[str, str]]:
        """
        Translates all news fields to other languages.
        
        Args:
            title: News title
            content: News content
            category: News category
            author: News author
            source_lang: Source language (default ru)
            
        Returns:
            Dictionary with translations: {lang: {title, content, category, author}}
        """
        translations = {}
        target_languages = ['en', 'kz'] if source_lang == 'ru' else ['ru', 'kz'] if source_lang == 'en' else ['ru', 'en']

        # Category translations dictionary
        category_translations = {
            'ru': {
                'Event': 'Событие',
                'Announcement': 'Объявление',
                'Academic': 'Академический',
                'Sports': 'Спорт'
            },
            'en': {
                'Event': 'Event',
                'Announcement': 'Announcement',
                'Academic': 'Academic',
                'Sports': 'Sports'
            },
            'kz': {
                'Event': 'Оқиға',
                'Announcement': 'Хабарландыру',
                'Academic': 'Академиялық',
                'Sports': 'Спорт'
            }
        }

        for target_lang in target_languages:
            try:
                translated_title = self.translate_text(title, source_lang, target_lang)
                translated_content = self.translate_text(content, source_lang, target_lang)
                
                # Use dictionary for category if available, otherwise translate
                if category in category_translations.get(target_lang, {}):
                    translated_category = category_translations[target_lang][category]
                else:
                    translated_category = self.translate_text(category, source_lang, target_lang)
                
                # Usually we don't translate author, but can be done if needed
                translated_author = author  # Keep author unchanged

                translations[target_lang] = {
                    'title': translated_title or title,
                    'content': translated_content or content,
                    'category': translated_category or category,
                    'author': translated_author
                }

            except Exception as e:
                logger.error(f"Error translating to {target_lang}: {str(e)}")
                # Use original values in case of error
                translations[target_lang] = {
                    'title': title,
                    'content': content,
                    'category': category,
                    'author': author
                }

        return translations

    def translate_product(self, name: str, description: str, category: str,
                         source_lang: str = 'ru') -> Dict[str, Dict[str, str]]:
        """
        Translates all product fields to other languages.
        
        Args:
            name: Product name
            description: Product description
            category: Product category
            source_lang: Source language (default ru)
            
        Returns:
            Dictionary with translations: {lang: {name, description, category}}
        """
        translations = {}
        target_languages = ['en', 'kz'] if source_lang == 'ru' else ['ru', 'kz'] if source_lang == 'en' else ['ru', 'en']

        # Product category translations dictionary
        category_translations = {
            'ru': {
                'Clothing': 'Одежда',
                'Accessories': 'Аксессуары',
                'Stationery': 'Канцелярия',
                'Books': 'Книги'
            },
            'en': {
                'Clothing': 'Clothing',
                'Accessories': 'Accessories',
                'Stationery': 'Stationery',
                'Books': 'Books'
            },
            'kz': {
                'Clothing': 'Киім',
                'Accessories': 'Аксессуарлар',
                'Stationery': 'Канцелярия',
                'Books': 'Кітаптар'
            }
        }

        for target_lang in target_languages:
            try:
                translated_name = self.translate_text(name, source_lang, target_lang)
                translated_description = self.translate_text(description, source_lang, target_lang)
                
                # Use dictionary for category if available, otherwise translate
                if category in category_translations.get(target_lang, {}):
                    translated_category = category_translations[target_lang][category]
                else:
                    translated_category = self.translate_text(category, source_lang, target_lang)

                translations[target_lang] = {
                    'name': translated_name or name,
                    'description': translated_description or description,
                    'category': translated_category or category
                }

            except Exception as e:
                logger.error(f"Error translating product to {target_lang}: {str(e)}")
                # Use original values in case of error
                translations[target_lang] = {
                    'name': name,
                    'description': description,
                    'category': category
                }

        return translations

    def is_available(self) -> bool:
        """Checks if translation service is available"""
        return self._translator is not None
