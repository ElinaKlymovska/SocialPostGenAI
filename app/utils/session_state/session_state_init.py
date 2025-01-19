import streamlit as st
from chat.conversation_chain import create_conversation_chain
from config.configuration import NUM_CHUNKS
from models.chromadb import init_chromadb, init_memory
from models.llm_model import init_chat_model


def init_session_state():
    """
    Ініціалізує стан сесії для Streamlit додатку.
    """
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    if "vectorstore" not in st.session_state or "llm" not in st.session_state:
        initialize_vectorstore_and_chain()

    if "processed_files" not in st.session_state:
        st.session_state["processed_files"] = set()


def initialize_vectorstore_and_chain():
    """
    Ініціалізує векторне сховище, LLM і ланцюг обробки розмов.
    """
    if "vectorstore" not in st.session_state:
        st.session_state["vectorstore"] = init_chromadb()

    if "llm" not in st.session_state:
        st.session_state["llm"] = init_chat_model()

    if "memory" not in st.session_state:
        st.session_state["memory"] = init_memory()

    st.session_state["chain"] = create_conversation_chain(
        st.session_state["llm"],
        st.session_state["vectorstore"].as_retriever(search_kwargs={"k": NUM_CHUNKS}),
        st.session_state["memory"]
    )


def reset_session_state():
    """
    Скидає стан сесії до початкового стану.
    """
    st.session_state["chat_history"] = []
    if "memory" in st.session_state:
        st.session_state["memory"].clear()
    st.rerun()
