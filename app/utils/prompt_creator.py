import streamlit as st
from deep_translator import GoogleTranslator
from gradio.tunneling import CHUNK_SIZE
from pypdf import PdfReader
from io import BytesIO
from langchain.text_splitter import RecursiveCharacterTextSplitter

from config.configuration import CHUNK_OVERLAP
from utils.toucher_llm_model import process_uploaded_image


LANGUAGE_CODES = {
    "en": "en",
    "uk": "uk",
}


def translate_keywords(keywords, target_language="en"):
    """
    Перекладає список ключових слів на обрану мову.

    Args:
        keywords (list): Список ключових слів.
        target_language (str): Мова перекладу.

    Returns:
        list: Перекладені ключові слова.
    """
    return [
        GoogleTranslator(source="auto", target=target_language).translate(word.strip())
        for word in keywords
    ]


def process_files(uploaded_files):
    """
    Обробляє завантажені файли (зображення або текст).

    Args:
        uploaded_files (list): Список завантажених файлів.

    Returns:
        tuple: Ключові слова із зображень та текстовий контекст із файлів.
    """
    image_labels = []
    file_context = ""  # Ініціалізація змінної

    for file in uploaded_files:
        if file.name not in st.session_state.processed_files:
            with st.spinner(f"Processing {file.name}..."):
                # Ініціалізація file_content для кожного файлу
                file_content = ""

                if file.type.startswith("image/"):
                    # Обробка зображень
                    image_labels.extend(process_uploaded_image(file))
                elif file.type == "application/pdf":
                    # Обробка PDF-файлів
                    pdf_reader = PdfReader(BytesIO(file.read()))
                    file_content = "\n".join(page.extract_text() for page in pdf_reader.pages)
                elif file.type.startswith("text/") or file.type == "text/plain":
                    # Обробка текстових файлів
                    file_content = file.read().decode()

                # Якщо контент отримано, додаємо його до vectorstore
                if file_content:
                    text_splitter = RecursiveCharacterTextSplitter(
                        chunk_size=CHUNK_SIZE,
                        chunk_overlap=CHUNK_OVERLAP,
                        separators=["\n\n", "\n", " ", ""]
                    )
                    chunks = text_splitter.split_text(file_content)

                    st.session_state.vectorstore.add_texts(
                        texts=chunks,
                        metadatas=[{"filename": file.name, "type": file.type}] * len(chunks)
                    )

                    st.session_state.processed_files.add(file.name)
                    st.success(f"Processed {file.name}")

                    # Переклад текстового контенту
                    file_context += GoogleTranslator(source="auto", target=LANGUAGE_CODES["en"]).translate(file_content)

    return image_labels, file_context


def prepare_prompt(keywords, tone, language, uploaded_files=None):
    """
    Формує промпт для генерації тексту на основі введених параметрів.

    Args:
        keywords (list): Список ключових слів.
        tone (str): Тональність тексту.
        language (str): Обрана мова.
        uploaded_files (list): Завантажені файли (опціонально).

    Returns:
        str: Підготовлений перекладений промпт.
    """
    translated_keywords = translate_keywords(keywords)
    image_labels, file_context = process_files(uploaded_files or [])

    # Додавання ключових слів із зображень
    if image_labels:
        translated_labels = translate_keywords(image_labels)
        translated_keywords.extend(translated_labels)

    # Формування фінального промпту
    prompt = (
        f"Create a {tone} social media post based on these keywords: {', '.join(translated_keywords)}."
        f" {file_context}"
    )
    return GoogleTranslator(source="auto", target=LANGUAGE_CODES[language]).translate(prompt)
