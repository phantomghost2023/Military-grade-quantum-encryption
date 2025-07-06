import json
import os

class Internationalization:
    def __init__(self, default_lang='en'):
        self.translations = {}
        self.current_lang = default_lang
        self.load_translations()

    def load_translations(self, lang_dir='locales'):
        """Loads translation files from the specified directory."""
        base_path = os.path.dirname(os.path.abspath(__file__))
        locales_path = os.path.join(base_path, lang_dir)
        
        if not os.path.exists(locales_path):
            os.makedirs(locales_path)

        for filename in os.listdir(locales_path):
            if filename.endswith('.json'):
                lang_code = os.path.splitext(filename)[0]
                filepath = os.path.join(locales_path, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        self.translations[lang_code] = json.load(f)
                except Exception as e:
                    print(f"Error loading translation file {filepath}: {e}")

    def set_language(self, lang_code):
        """Sets the current language if translations are available for it."""
        if lang_code in self.translations:
            self.current_lang = lang_code
            return True
        return False

    def get_translation(self, key, lang_code=None):
        """Retrieves the translation for a given key in the current or specified language."""
        lang = lang_code if lang_code else self.current_lang
        return self.translations.get(lang, {}).get(key, key)

# Example usage (for testing/demonstration)
if __name__ == '__main__':
    # Create a dummy locales directory and translation files
    if not os.path.exists('locales'):
        os.makedirs('locales')

    with open('locales/en.json', 'w', encoding='utf-8') as f:
        json.dump({
            "hello": "Hello",
            "welcome": "Welcome to our application!",
            "greeting_name": "Hello, {name}!"
        }, f, indent=4)

    with open('locales/es.json', 'w', encoding='utf-8') as f:
        json.dump({
            "hello": "Hola",
            "welcome": "¡Bienvenido a nuestra aplicación!",
            "greeting_name": "¡Hola, {name}!"
        }, f, indent=4)

    i18n = Internationalization()
    print(f"Current language: {i18n.current_lang}")
    print(i18n.get_translation("hello"))
    print(i18n.get_translation("welcome"))
    print(i18n.get_translation("greeting_name").format(name="Alice"))

    i18n.set_language('es')
    print(f"Current language: {i18n.current_lang}")
    print(i18n.get_translation("hello"))
    print(i18n.get_translation("welcome"))
    print(i18n.get_translation("greeting_name").format(name="Bob"))

    # Test a missing key
    print(i18n.get_translation("missing_key"))

    # Test a missing language
    i18n.set_language('fr')
    print(f"Current language after trying 'fr': {i18n.current_lang}")
    print(i18n.get_translation("hello"))