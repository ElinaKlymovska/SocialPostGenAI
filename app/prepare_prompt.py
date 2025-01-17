from deep_translator import GoogleTranslator

from utils import process_uploaded_image

LANGUAGE_CODES = {
    "en": "en",
    "uk": "uk",
}


def prepare_prompt(keywords, tone, language, uploaded_files=None):
    """
    Підготовка промпту для генерації тексту із врахуванням мови, тональності, ключових слів,
    об'єктів із зображень та вмісту текстових файлів.

    :param keywords: Список ключових слів.
    :param tone: Тональність тексту.
    :param language: Обрана мова.
    :param uploaded_files: Вміст текстових файлів (рядок) або Об'єкти, знайдені в зображеннях (список).
    :return: Підготовлений промпт.
    """
    # Переклад ключових слів
    keywords = [
        GoogleTranslator(source="auto", target=LANGUAGE_CODES["en"]).translate(word.strip())
        for word in keywords
    ]

    # Process uploaded files
    image_labels = []
    file_content = ""
    if uploaded_files:
        for file in uploaded_files:
            if file.type.startswith("image/"):
                labels = process_uploaded_image(file)
                image_labels.extend(labels)
            else:
                file_content += file.read().decode()

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
