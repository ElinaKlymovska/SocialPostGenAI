from telegram import Update, Bot
from telegram.ext import CallbackContext

from utils.toucher_llm_model import converse_with_titan


class TelegramAdapter:
    """
    Адаптер для інтеграції з Telegram-ботом.
    """

    def __init__(self, token: str):
        """
        Ініціалізує адаптер з токеном Telegram API.

        Args:
            token (str): Токен Telegram-бота.
        """
        self.bot = Bot(token)

    def start_command(self, update: Update, context: CallbackContext):
        """
        Відправляє привітальне повідомлення при старті.
        """
        update.message.reply_text("Hello! I'm your AI assistant. Ask me anything!")

    def handle_message(self, update: Update, context: CallbackContext):
        """
        Обробляє повідомлення від користувача.

        Args:
            update (Update): Об'єкт повідомлення Telegram.
            context (CallbackContext): Контекст повідомлення.
        """
        user_message = update.message.text
        response = self.generate_response(user_message)
        update.message.reply_text(response)

    def generate_response(self, user_message: str) -> str:
        """
        Генерує відповідь на основі вхідного повідомлення.

        Args:
            user_message (str): Повідомлення від користувача.

        Returns:
            str: Згенерована відповідь.
        """
        response, _ = converse_with_titan(user_message, [])
        return response
