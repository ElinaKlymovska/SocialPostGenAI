import streamlit as st
from langchain_community.chat_models import BedrockChat
from config.configuration import BEDROCK_MODEL, TEMPERATURE, AWS_REGION


@st.cache_resource(show_spinner=False)
def init_chat_model():
    """
    Ініціалізує модель чату на основі Amazon Bedrock.

    Returns:
        BedrockChat: Ініціалізована модель чату.
    """
    return BedrockChat(
        model_id=BEDROCK_MODEL,
        model_kwargs={"temperature": TEMPERATURE},
        region_name=AWS_REGION
    )
