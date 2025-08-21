from langchain_groq import ChatGroq
from langchain.chains import create_retrieval_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import Runnable
from langchain_core.vectorstores import VectorStore
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from config.config import AppConfig

# --- 1. Define Prompt Templates for Clarity ---

CONTEXTUALIZER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "Given the chat history and user question, rewrite it as a standalone question."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

# --- THIS IS THE NEW, IMPROVED PROMPT ---
QA_PROMPT = ChatPromptTemplate.from_messages([
    ("system", (
        "You are a friendly and helpful e-commerce assistant named 'Shop Smart AI'. "
        "Your goal is to help users by answering questions about products using the provided context of customer reviews. "
        "Strictly base your answers on the information within the context. "
        "If the context does not contain information to answer the question, do not make anything up. "
        "Instead, politely say that you couldn't find information on that specific product in the reviews and suggest they ask about something else, like the headsets or earphones available in the dataset.\n\n"
        "CONTEXT:\n{context}"
    )),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

# In-memory store for chat histories
store = {}

def get_session_history(session_id: str) -> ChatMessageHistory:
    """
    Retrieves the chat history for a given session ID.
    If no history exists, a new one is created.
    """
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# --- 2. Create the RAG Chain ---

def create_rag_chain(vector_store: VectorStore) -> Runnable:
    """
    Creates a conversational RAG chain.

    Args:
        vector_store: A configured vector store instance.

    Returns:
        A LangChain Runnable that manages the conversation flow.
    """
    # 1. Initialize the LLM
    model = ChatGroq(model_name=AppConfig.RAG_MODEL, temperature=AppConfig.RAG_TEMPERATURE)

    # 2. Create the retriever
    retriever = vector_store.as_retriever(search_kwargs={"k": AppConfig.RAG_RETRIEVER_K})

    # 3. Create the history-aware retriever
    history_aware_retriever = create_history_aware_retriever(
        llm=model,
        retriever=retriever,
        prompt=CONTEXTUALIZER_PROMPT
    )

    # 4. Create the question-answering chain
    question_answer_chain = create_stuff_documents_chain(
        llm=model,
        prompt=QA_PROMPT
    )

    # 5. Combine them into a final retrieval chain
    rag_chain = create_retrieval_chain(
        retriever=history_aware_retriever,
        combine_docs_chain=question_answer_chain
    )

    # 6. Add history management
    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )

    return conversational_rag_chain