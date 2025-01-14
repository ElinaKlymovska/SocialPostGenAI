from deep_translator import GoogleTranslator

LANGUAGE_CODES = {
    "en": "en",
    "uk": "uk",
}


def prepare_prompt(keywords, tone, language, image_labels=None, file_content=None):
    """
    Підготовка промпту для генерації тексту із врахуванням мови, тональності, ключових слів,
    об'єктів із зображень та вмісту текстових файлів.

    :param keywords: Список ключових слів.
    :param tone: Тональність тексту.
    :param language: Обрана мова.
    :param image_labels: Об'єкти, знайдені в зображеннях (список).
    :param file_content: Вміст текстових файлів (рядок).
    :return: Підготовлений промпт.
    """
    # Переклад ключових слів
    keywords = [
        GoogleTranslator(source="auto", target=LANGUAGE_CODES["en"]).translate(word.strip())
        for word in keywords
    ]

    # Додавання об'єктів із зображень
    if image_labels:
        translated_labels = [
            GoogleTranslator(source="auto", target=LANGUAGE_CODES["en"]).translate(label.strip())
            for label in image_labels
        ]
        keywords.extend(translated_labels)

    # Формування тексту з текстових файлів
    file_context = ""
    if file_content:
        file_context = GoogleTranslator(source="auto", target=LANGUAGE_CODES["en"]).translate(file_content)
        file_context = f"Here is additional context extracted from uploaded files: {file_context}"

    # Формування фінального промпту
    prompt = (
        f"Create a {tone} social media post based on these keywords: {', '.join(keywords)}."
        f" {file_context}"
    )
    # Переклад промпту на обрану мову
    prompt_translated = GoogleTranslator(source="auto", target=LANGUAGE_CODES[language]).translate(prompt)

    return prompt_translated
