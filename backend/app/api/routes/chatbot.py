from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.api.dependencies import CurrentUser, SessionDependency
from app.chatbot.chatbot_core import Chatbot
from app.models import ChatHistory, ChatHistoryRequest, Thread, ThreadCreate, UserMessage

router = APIRouter(prefix="/chatbot", tags=["chatbot"])
chatbot = Chatbot()


@router.post("/chat", summary="Send a message to the chatbot")
def chat_endpoint(
    user_message: UserMessage,
    session: SessionDependency,
    current_user: CurrentUser,
):
    """
    Send a message to the chatbot and receive a response.

    Args:
        user_message: The message from the user, including thread ID.

    Returns:
        The response from the chatbot, with Markdown converted to HTML.

    Raises:
        HTTPException: If there's an error processing the message.
    """
    try:
        thread_id = user_message.thread_id
        if thread_id is None:
            # Create a new thread for the user
            thread = Thread.model_validate(ThreadCreate(title="New Thread"), update={"user_id": current_user.id})
            session.add(thread)
            session.commit()
            session.refresh(thread)
            thread_id = thread.id

        response = chatbot.process_message(user_message.content, str(thread_id))

        return {"response": response, "thread_id": str(thread_id)}
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@router.post("/chat-history", summary="Get chat history")
def chat_history_endpoint(
    request: ChatHistoryRequest,
    session: SessionDependency,
    current_user: CurrentUser,
):
    """
    Retrieve the chat history for a specific thread.

    Args:
        request: The request containing the thread ID.

    Returns:
        The chat history for the specified thread.

    Raises:
        HTTPException: If there's an error retrieving the chat history.
    """
    try:
        if request.thread_id is None:
            raise HTTPException(status_code=400, detail="Thread ID is required.")

        thread_id = request.thread_id
        statement = select(Thread).where(Thread.id == thread_id, Thread.user_id == current_user.id)
        thread = session.exec(statement).first()
        if not thread:
            raise HTTPException(status_code=404, detail="Thread not found.")
        chat_history = chatbot.get_chat_history(str(thread_id))
        return ChatHistory(thread_id=thread_id, messages=chat_history)
    except HTTPException as http_error:
        raise http_error
    except Exception as error:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")
