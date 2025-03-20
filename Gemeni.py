import google.generativeai as genai
import configparser

class GeminiIntegrationModule:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        genai.configure(api_key=config.get('gemeni', 'api_key')) # Конфигурируем Gemini с API ключом

        self.model = genai.GenerativeModel('gemini-2.0-flash') # Выбираем модель Gemini Pro (бесплатная)

    def summarize_text(self, text):
        """Суммаризирует текст с помощью Gemini."""
        try:
            response = self.model.generate_content(f"Кратко и по делу просуммируй следующий текст:\n\n{text}")
            return response.text
        except Exception as e:
            print(f"❌ Ошибка при суммаризации через Gemini: {e}")
            return None
