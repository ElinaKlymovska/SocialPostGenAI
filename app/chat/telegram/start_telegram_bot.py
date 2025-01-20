from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes
from telegram.ext import filters

from chat.telegram.telegram_adapter import TelegramAdapter


def start_telegram_bot(token: str):
    """
    Запускає Telegram-бота.

    Args:
        token (str): Токен Telegram API.
    """
    adapter = TelegramAdapter(token)

    # Використовуємо ApplicationBuilder для побудови програми
    application = ApplicationBuilder().token(token).build()

    # Додаємо обробники команд і повідомлень
    application.add_handler(CommandHandler("start", adapter.start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, adapter.handle_message))

    print("Telegram bot is running...")
    application.run_polling()
