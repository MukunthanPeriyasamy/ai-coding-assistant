from backend.models import llm
from backend.prompts import advanced_prompt, beginner_prompt
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_groq import ChatGroq

# Store for chat message histories, keyed by session_id
chat_history_store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """Get or create a chat message history for a given session ID."""
    if session_id not in chat_history_store:
        chat_history_store[session_id] = InMemoryChatMessageHistory()
    return chat_history_store[session_id]

# Create prompt templates with message history placeholder
advanced_prompt_template = ChatPromptTemplate.from_messages([
    ("system", advanced_prompt),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}")
])

beginner_prompt_template = ChatPromptTemplate.from_messages([
    ("system", beginner_prompt),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}")
])

# Create chains with message history
advanced_chain = advanced_prompt_template | llm
beginner_chain = beginner_prompt_template | llm

# Wrap chains with message history
advanced_chain_with_history = RunnableWithMessageHistory(
    advanced_chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history"
)

beginner_chain_with_history = RunnableWithMessageHistory(
    beginner_chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history"
)

def ai_tutor(prompt: str, session_id: str = "default"):
    """
    Advanced AI tutor with streaming support.
    """
    for chunk in advanced_chain_with_history.stream(
        {"question": prompt},
        config={"configurable": {"session_id": session_id}}
    ):
        if chunk.content:
            yield chunk.content

def ai_beginner_tutor(prompt: str, session_id: str = "default"):
    """
    Beginner AI tutor with streaming support.
    """
    for chunk in beginner_chain_with_history.stream(
        {"question": prompt},
        config={"configurable": {"session_id": session_id}}
    ):
        if chunk.content:
            yield chunk.content