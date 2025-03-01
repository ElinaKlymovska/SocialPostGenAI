import boto3


def process_uploaded_image(uploaded_file):
    """
    Використовує AWS Rekognition для аналізу зображень.

    Args:
        uploaded_file: Завантажений файл зображення.

    Returns:
        list: Список імен знайдених об'єктів.
    """
    rekognition_client = boto3.client("rekognition")
    try:
        image_bytes = uploaded_file.read()
        response = rekognition_client.detect_labels(
            Image={"Bytes": image_bytes},
            MaxLabels=10,
            MinConfidence=75
        )
        return [label["Name"] for label in response.get("Labels", [])]
    except Exception as e:
        print(f"Error processing image: {e}")
        return []


def converse_with_titan(user_message, conversation_history):
    """
    Викликає API Bedrock для підтримки розмови з моделлю Amazon Titan.

    Args:
        user_message (str): Повідомлення користувача.
        conversation_history (list): Історія переписки.

    Returns:
        tuple: Відповідь моделі та оновлена історія переписки.
    """
    try:
        brt = boto3.client("bedrock-runtime")
        model_id = "amazon.titan-tg1-large"

        # Формуємо історію розмови
        conversation = [
            {"role": msg["role"], "content": [{"text": msg["content"]}]}
            for msg in conversation_history
        ]
        conversation.append({"role": "user", "content": [{"text": user_message}]})

        request_payload = {
            "modelId": model_id,
            "messages": conversation,
            "inferenceConfig": {
                "maxTokens": 300,
                "temperature": 0.7
            }
        }

        response = brt.converse(**request_payload)
        assistant_response = (
            response.get("output", {})
            .get("message", {})
            .get("content", [{}])[0]
            .get("text", "No response received.")
        )

        # Додаємо відповідь моделі до історії
        conversation_history.append({
            "role": "assistant",
            "content": [{"text": assistant_response}]
        })
        return assistant_response, conversation_history

    except Exception as e:
        print(f"Error during conversation: {e}")
        return f"Error: {e}", conversation_history
