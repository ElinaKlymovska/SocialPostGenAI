import streamlit as st

from utils.prompt_creator import prepare_prompt
from utils.session_state.session_state_init import init_session_state, reset_session_state
from utils.toucher_llm_model import converse_with_titan


def display_app_header():
    """
    Відображає заголовок і опис додатку.
    """
    st.title("AI-powered Content Generator")
    st.markdown("""
    This AI assistant can:
    - Generate engaging and creative social media content tailored to your needs
    - Provide suggestions for captions, hashtags, and post formats
    - Analyze uploaded images or text to create relevant and appealing content
    - Maintain context across the conversation to ensure consistent branding and tone
    - Help brainstorm ideas for posts, campaigns, and creative strategies
    """)


def display_generated_text(response):
    """
    Відображає згенерований текст посередині екрану.

    Args:
        response (str): Згенерований текст.
    """
    with st.container():
        st.subheader("Generated Content")
        st.markdown(
            f"""
            <div style="text-align: center; font-size: 18px; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                {response}
            </div>
            """,
            unsafe_allow_html=True
        )

def display_sidebar():
    """
    Відображає параметри в боковій панелі для налаштування генерації контенту.
    """
    with st.sidebar:
        st.header("Set parameters:")
        uploaded_files = st.file_uploader(
            "Upload text or image files",
            type=["txt", "pdf", "png", "jpg"],
            accept_multiple_files=True
        )
        keywords = st.text_input("Enter keywords:")
        language = st.selectbox("Select language:", ["en", "uk"])
        tone = st.selectbox("Select tone:", ["friendly", "formal", "creative"])

        if st.button("Generate Content"):
            prompt = prepare_prompt(keywords.split(","), tone, language, uploaded_files)
            response, _ = converse_with_titan(prompt, [])
            display_generated_text(response)

        if st.button("Clear Chat History"):
            reset_session_state()


def display_chat_interface():
    """
    Відображає інтерфейс чату для користувача та асистента.
    """
    chat_container = st.container()
    with chat_container:
        # Відображення історії чату
        for message in st.session_state.chat_history:
            with st.chat_message("assistant" if message["is_assistant"] else "user"):
                st.write(message["content"])
                if message.get("sources"):
                    with st.expander("View sources"):
                        for source in message["sources"]:
                            st.markdown(f"""
                            **From**: {source['filename']}
                            **Text**: \n\n{source['text']}
                            ---
                            """)

    # Вхідне повідомлення від користувача
    if question := st.chat_input("Add additional instructions"):
        handle_user_input(question)


def handle_user_input(question):
    """
    Обробляє введення користувача та оновлює чат.

    Args:
        question (str): Повідомлення користувача.
    """
    # Додаємо повідомлення користувача до чату
    st.session_state.chat_history.append({"is_assistant": False, "content": question})

    try:
        result = st.session_state.chain({"question": question})
        answer = result["answer"]
        sources = []

        if result.get("source_documents"):
            for doc in result["source_documents"]:
                sources.append({
                    "filename": doc.metadata.get("filename", "Unknown"),
                    "text": doc.page_content
                })

        # Додаємо відповідь асистента до чату
        st.session_state.chat_history.append({
            "is_assistant": True,
            "content": answer,
            "sources": sources if sources else None
        })

        # Оновлюємо інтерфейс
        st.rerun()

    except Exception as e:
        st.error(f"Error: {str(e)}")


# Головна логіка
if __name__ == "__main__":
    init_session_state()
    display_app_header()
    display_sidebar()
    display_chat_interface()
