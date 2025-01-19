from collections import defaultdict
from datetime import datetime, timedelta


class MessageAggregator:
    """
    Клас для агрегування повідомлень користувачів протягом певного часового вікна.
    """

    DEFAULT_WINDOW_SIZE = 5  # Розмір вікна за замовчуванням (у секундах)

    def __init__(self, window_size: int = DEFAULT_WINDOW_SIZE):
        """
        Ініціалізує агрегатор повідомлень.

        Args:
            window_size (int): Часове вікно для агрегування повідомлень у секундах.
        """
        self.messages = defaultdict(list)
        self.window_size = timedelta(seconds=window_size)

    def add_message(self, user_id: str, message: str):
        """
        Додає нове повідомлення для вказаного користувача.

        Args:
            user_id (str): Ідентифікатор користувача.
            message (str): Текст повідомлення.
        """
        self.messages[user_id].append({"text": message, "timestamp": datetime.now()})

    def should_process(self, user_id: str) -> bool:
        """
        Перевіряє, чи достатньо часу пройшло для обробки повідомлень користувача.

        Args:
            user_id (str): Ідентифікатор користувача.

        Returns:
            bool: True, якщо потрібно обробити повідомлення, інакше False.
        """
        if user_id not in self.messages or not self.messages[user_id]:
            return False
        last_message_time = self.messages[user_id][-1]["timestamp"]
        return datetime.now() - last_message_time > self.window_size

    def get_aggregated_message(self, user_id: str) -> str:
        """
        Повертає агреговане повідомлення для вказаного користувача.

        Args:
            user_id (str): Ідентифікатор користувача.

        Returns:
            str: Агрегований текст повідомлень.
        """
        if user_id not in self.messages:
            return ""

        aggregated_messages = " ".join(
            msg["text"] for msg in self.messages[user_id]
        )
        self.messages[user_id].clear()  # Очистка після обробки
        return aggregated_messages
