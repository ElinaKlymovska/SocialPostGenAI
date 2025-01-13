from deep_translator import GoogleTranslator
from enum import Enum

# Список мов, які підтримуються
LANGUAGE_CODES = {
    "Українська": "uk",
    "Англійська": "en",
    "Польська": "pl",
    "Італійська": "it",
}

class Tone(Enum):
    FRIENDLY = "friendly"
    FORMAL = "formal"
    NEUTRAL = "neutral"
    CREATIVE = "creative"

def prepare_prompt(keywords, tone, language):
    """
    Підготовка промпту для генерації тексту із врахуванням мови, тональності та ключових слів.

    :param keywords: Список ключових слів.
    :param tone: Значення з Tone (тональність тексту).
    :param language: Обрана мова.
    :return: Підготовлений промпт.
    """
    # Переклад ключових слів на вибрану мову
    translated_keywords = [
        GoogleTranslator(source="auto", target=LANGUAGE_CODES[language]).translate(word.strip())
        for word in keywords
    ]

    # Формування промпта англійською мовою
    prompt = f"Write a {tone.value} social media text based on these keywords: {', '.join(translated_keywords)}."

    # Якщо мова не англійська, перекладаємо весь промпт
    if language != "Англійська":
        prompt = GoogleTranslator(source="en", target=LANGUAGE_CODES[language]).translate(prompt)

    return prompt, translated_keywords
