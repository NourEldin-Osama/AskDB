from fastapi import APIRouter, HTTPException

from app.chatbot.chatbot_core import Chatbot
from app.models import ChatMessage

router = APIRouter(prefix="/chatbot", tags=["chatbot"])
chatbot = Chatbot()


@router.post("/chat", summary="Send a message to the chatbot")
def chat_endpoint(chat_message: ChatMessage):
    """
    Send a message to the chatbot and receive a response.

    Args:
        chat_message: The message from the user, including thread ID.

    Returns:
        The response from the chatbot, with Markdown converted to HTML.

    Raises:
        HTTPException: If there's an error processing the message.
    """
    try:
        response = chatbot.process_message(chat_message.message, str(chat_message.thread_id))

        return {"response": response}
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
