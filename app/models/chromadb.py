import os
import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# Константи для ChromaDB
PERSIST_DIR = "db"  # Директорія для збереження ChromaDB
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Модель для створення ембедингів


def ensure_persistence_directory():
    """
    Забезпечує існування директорії для збереження даних ChromaDB.
    """
    os.makedirs(PERSIST_DIR, exist_ok=True)


@st.cache_resource(show_spinner=False)
def init_embeddings():
    """
    Ініціалізує ембединг-модель для векторного представлення тексту.

    Returns:
        HuggingFaceEmbeddings: Ембединг-функція.
    """
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )


@st.cache_resource(show_spinner=False)
def init_chromadb():
    """
    Ініціалізує ChromaDB з підтримкою персистентності та трансформерних ембедингів.

    Returns:
        Chroma: Векторне сховище ChromaDB.
    """
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    ensure_persistence_directory()

    embeddings = init_embeddings()

    return Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings,
        collection_name="documents"
    )


@st.cache_resource(show_spinner=False)
def init_memory():
    """
    Ініціалізує буферну пам'ять для збереження історії розмов.

    Returns:
        ConversationBufferMemory: Пам'ять для збереження історії чату.
    """
    return ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )
