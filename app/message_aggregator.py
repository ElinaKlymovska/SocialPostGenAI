from collections import defaultdict
from datetime import datetime, timedelta

# Configuration
AGGREGATION_WINDOW = 5

class MessageAggregator:
    def __init__(self, window_size: int = AGGREGATION_WINDOW):
        self.messages = defaultdict(list)
        self.last_processed = {}
        self.window_size = timedelta(seconds=window_size)

    def add_message(self, user_id: str, message: str):
        current_time = datetime.now()
        self.messages[user_id].append({"text": message, "timestamp": current_time})

    def should_process(self, user_id: str) -> bool:
        if user_id not in self.messages:
            return False
        last_message_time = self.messages[user_id][-1]["timestamp"]
        return datetime.now() - last_message_time > self.window_size

    def get_aggregated_message(self, user_id: str) -> str:
        if user_id not in self.messages:
            return ""
        messages = self.messages[user_id]
        self.messages[user_id] = []  # Очистити після отримання
        return " ".join(msg["text"] for msg in messages)