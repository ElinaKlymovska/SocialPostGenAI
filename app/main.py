import streamlit as st
from prepare_prompt import LANGUAGE_CODES, prepare_prompt, Tone
from utils import get_rekognition_client, converse_with_titan
from PIL import Image

# Налаштування AWS Rekognition клієнта
rekognition = get_rekognition_client()

# Збереження історії розмови
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# Заголовок додатка
st.title("AI Social Media Post Generator with Correction")
st.subheader("Генерація та корекція контенту для соціальних мереж")

# Вибір мови
language = st.selectbox("Оберіть мову тексту:", list(LANGUAGE_CODES.keys()))

# Вибір тональності
tone = st.selectbox("Оберіть тональність:", [tone.name.capitalize() for tone in Tone])  # Виводимо назви з великої літери
tone_value = Tone[tone.upper()]  # Приводимо текст до верхнього регістру для enum

# Поле для введення ключових слів
custom_keywords = st.text_input("Введіть власні ключові слова (через кому):")

# Завантаження зображення
uploaded_file = st.file_uploader("Завантажте зображення", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Відображення завантаженого зображення
    image = Image.open(uploaded_file)
    st.image(image, caption="Завантажене зображення", use_container_width=True)

    # Розпізнавання об'єктів
    st.write("Розпізнавання об'єктів...")
    response = rekognition.detect_labels(
        Image={'Bytes': uploaded_file.getvalue()},
        MaxLabels=5,
        MinConfidence=75
    )

    # Отримання об'єктів
    labels = [label['Name'] for label in response['Labels']]
    st.write("Ідентифіковані об'єкти:", ", ".join(labels))

    # Об'єднання ключових слів
    keywords = labels + (custom_keywords.split(",") if custom_keywords else [])

    if keywords:
        # Формування промпту
        prompt, translated_keywords = prepare_prompt(keywords, tone_value, language)

        # Відправлення промпту до Bedrock
        st.write("Згенерований промпт:", prompt)
        print("Generated prompt:", prompt)

        if st.button("Генерувати текст"):
            generated_text, st.session_state.conversation_history = converse_with_titan(
                user_message=prompt,
                conversation_history=st.session_state.conversation_history,
            )
            st.session_state.generated_text = generated_text

        # Виведення та редагування тексту
        if "generated_text" in st.session_state:
            st.text_area(
                "Згенерований текст:",
                value=st.session_state.generated_text,
                height=150,
                key="editable_text",
            )

        # Надіслати відредагований текст
        if st.button("Доопрацювати текст"):
            user_edited_text = st.session_state.editable_text
            updated_text, st.session_state.conversation_history = converse_with_titan(
                user_message=user_edited_text,
                conversation_history=st.session_state.conversation_history,
            )
            st.session_state.generated_text = updated_text
            st.success("Текст успішно оновлено!")
else:
    st.info("Будь ласка, завантажте зображення для початку.")
