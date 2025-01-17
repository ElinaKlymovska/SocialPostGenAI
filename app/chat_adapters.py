from abc import ABC, abstractmethod

class ChatEngineAdapter(ABC):
    @abstractmethod
    def receive_message(self, raw_data: dict) -> dict:
        """Обробка отриманого повідомлення."""
        pass

    @abstractmethod
    def send_message(self, response: dict, user_id: str) -> None:
        """Надсилання відповіді користувачу."""
        pass


class WebSocketAdapter(ChatEngineAdapter):
    async def handle_events(self, event_data: dict):
        event_type = event_data.get("type")
        if event_type == "connect":
            # Логіка підключення
            pass
        elif event_type == "disconnect":
            # Логіка відключення
            pass
