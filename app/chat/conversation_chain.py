from langchain.prompts import ChatPromptTemplate
from langchain.chains import ConversationalRetrievalChain


def create_conversation_chain(llm, retriever, memory):
    """
    Створює ланцюг для обробки розмови з використанням LLM, ретривера та пам'яті.

    Args:
        llm: Об'єкт мовної моделі (LLM).
        retriever: Ретрівер для пошуку контексту в документах.
        memory: Об'єкт пам'яті для збереження історії розмов.

    Returns:
        ConversationalRetrievalChain: Ланцюг обробки розмови.
    """
    template = """You are an AI-powered virtual tour guide who specializes in:
    1. Explaining the historical, cultural, or geological significance of objects.
    2. Generating engaging step-by-step visualizations of processes (e.g., mountain formation, architectural construction).
    3. Providing detailed and concise answers to users' questions about landmarks, artworks, and natural phenomena.
    4. Always being accurate, polite, and engaging in your responses.
    5. Using prior context from the conversation and any uploaded images or data to improve responses.

    Current conversation:
    {chat_history}

    Identified object or context:
    {context}

    User's question:
    {question}

    Assistant:"""

    prompt = ChatPromptTemplate.from_template(template)

    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": prompt},
        return_source_documents=True,
        verbose=True
    )
