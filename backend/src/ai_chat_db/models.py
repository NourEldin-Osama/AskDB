from sqlmodel import Field, SQLModel


class ChatMessage(SQLModel):
    message: str = Field(
        ...,
        description="Message content",
        schema_extra={"examples": ["Hello, how are you?", "What is the weather today?"]},
    )
    thread_id: str = Field(
        ...,
        description="Thread ID for the conversation",
        schema_extra={"examples": ["1", "2"]},
    )
