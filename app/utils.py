import boto3
import os
import json
from botocore.config import Config


def get_rekognition_client():
    """
    Ініціалізує клієнт AWS Rekognition.
    """
    return boto3.client(
        'rekognition',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION', 'us-east-1')
    )


def converse_with_titan(user_message, conversation_history=None, max_tokens=300):
    """
    Використовує Amazon Bedrock Converse API для генерації тексту з багатокроковою розмовою.

    :param user_message: Нове повідомлення користувача.
    :param conversation_history: Історія попередніх повідомлень.
    :param max_tokens: Максимальна кількість токенів для відповіді.
    :return: Згенерований текст і оновлена історія розмови.
    """
    client = boto3.client(
        "bedrock-runtime",
        region_name="us-east-1",  # Вкажіть правильний регіон
    )

    # Починаємо нову розмову, якщо історія порожня
    if not conversation_history:
        conversation_history = []

    # Додаємо нове повідомлення до історії
    if not conversation_history or conversation_history[-1]["role"] == "assistant":
        conversation_history.append({"role": "user", "content": [{"text": user_message}]})
    else:
        return "Error: A user message cannot follow another user message.", conversation_history

    try:
        print("Sending conversation to Bedrock with the following payload:")
        print(json.dumps(conversation_history, indent=4))

        response = client.converse(
            modelId="amazon.titan-tg1-large",  # Змініть ID моделі за потреби
            messages=conversation_history,
            inferenceConfig={
                "maxTokens": max_tokens,
                "temperature": 0.7,
                "topP": 0.9,
            },
        )

        # Розбираємо відповідь
        response_text = response["output"]["message"]["content"][0]["text"]
        print(f"Generated text: {response_text}")

        # Додаємо відповідь моделі до історії
        conversation_history.append({"role": "assistant", "content": [{"text": response_text}]})

        return response_text, conversation_history
    except Exception as e:
        print(f"Error during conversation: {e}")
        return f"Error: {e}", conversation_history
