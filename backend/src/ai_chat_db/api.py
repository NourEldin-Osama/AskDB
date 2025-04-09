from fastapi import FastAPI, HTTPException
from sqlmodel import Session, SQLModel, create_engine, select

from ai_chat_db.Chatbot import graph
from ai_chat_db.config import settings
from ai_chat_db.models import ChatMessage
from markdown_it import MarkdownIt

md = MarkdownIt()

app = FastAPI(title="Chatbot API", description="API to interact with the chatbot", version="1.0.0")

# # Setup SQLModel engine using the database URL from settings
# engine = create_engine(settings.database_url, echo=False)


# # Create all tables on startup if they don't exist
# @app.on_event("startup")
# def on_startup():
#     SQLModel.metadata.create_all(engine)


@app.post("/chat", summary="Send a message to the chatbot")
def chat_endpoint(chat_message: ChatMessage):
    """
    Send a message to the chatbot and receive a response.
    """
    try:
        config = {"configurable": {"thread_id": chat_message.thread_id}}
        response = graph.invoke({"messages": [{"role": "user", "content": chat_message.message}]}, config)
        response_text = response["messages"][-1].content  # Get the last message from the response
        # Convert Markdown to HTML
        response_text = md.render(response_text)
        return {"response": response_text}
    except Exception as error:
        raise HTTPException(status_code=500, detail=error)


if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI app using Uvicorn server
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
