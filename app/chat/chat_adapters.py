from abc import ABC, abstractmethod


class ChatEngineAdapter(ABC):
    """
    Базовий клас адаптера для роботи з чат-движками.
    """

    @abstractmethod
    def receive_message(self, raw_data: dict) -> dict:
        """
        Обробляє отримане повідомлення.

        Args:
            raw_data (dict): Вхідні дані повідомлення.

        Returns:
            dict: Оброблене повідомлення у форматі ключ-значення.
        """
        pass

    @abstractmethod
    def send_message(self, response: dict, user_id: str) -> None:
        """
        Відправляє повідомлення користувачу.

        Args:
            response (dict): Відповідь, яка буде відправлена.
            user_id (str): Ідентифікатор користувача.
        """
        pass


class WebSocketAdapter(ChatEngineAdapter):
    """
    Адаптер для роботи з WebSocket подіями.
    """

    async def handle_events(self, event_data: dict):
        """
        Обробляє події WebSocket.

        Args:
            event_data (dict): Дані події WebSocket.
        """
        event_type = event_data.get("type")
        if event_type == "connect":
            self.handle_connect()
        elif event_type == "disconnect":
            self.handle_disconnect()

    def handle_connect(self):
        """
        Логіка для обробки підключення.
        """
        print("User connected")

    def handle_disconnect(self):
        """
        Логіка для обробки відключення.
        """
        print("User disconnected")
