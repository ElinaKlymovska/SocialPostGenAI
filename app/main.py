from streamlit_ui.ui import display_app_sidebar, display_main_interface, display_chat_interface, \
    display_telegram_integration
from utils.session_state.session_state_init import init_session_state


if __name__ == "__main__":
    init_session_state()

    # Відображення бокової панелі
    display_app_sidebar()
    display_telegram_integration()

    # Основний функціонал посередині
    display_main_interface()

    # Інтерфейс чату
    display_chat_interface()
