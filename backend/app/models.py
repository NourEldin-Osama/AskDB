from datetime import datetime
from uuid import UUID, uuid4

import sqlalchemy as sa
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


class TimestampMixin(SQLModel):
    created_at: datetime | None = Field(
        default=None,
        sa_type=sa.DateTime(timezone=True),
        sa_column_kwargs={"server_default": sa.func.now()},
        nullable=False,
    )

    updated_at: datetime | None = Field(
        default=None,
        sa_type=sa.DateTime(timezone=True),
        sa_column_kwargs={"server_default": sa.func.now(), "onupdate": sa.func.now()},
    )


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# Database model, database table inferred from class name
class User(UserBase, TimestampMixin, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    hashed_password: str
    threads: list["Thread"] = Relationship(back_populates="user", cascade_delete=True)


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: UUID
    created_at: datetime | None
    updated_at: datetime | None


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


class ThreadBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)


class ThreadCreate(ThreadBase):
    pass


class ThreadUpdate(SQLModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)


class Thread(ThreadBase, TimestampMixin, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    user_id: UUID = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")
    user: User | None = Relationship(back_populates="threads")


class ThreadPublic(ThreadBase):
    id: UUID
    user_id: UUID
    created_at: datetime | None
    updated_at: datetime | None


class ThreadsPublic(SQLModel):
    data: list[ThreadPublic]
    count: int


# Generic response
class Response(SQLModel):
    message: str


class Message(SQLModel):
    role: str | None = Field(default=None)
    content: str


class UserMessage(Message):
    role: str = Field(default="user")
    content: str = Field(
        description="Message content from the user",
        schema_extra={"examples": ["Hello, how can I help you?"]},
    )
    thread_id: UUID | None = Field(
        default=None,
        description="Thread ID for the conversation (optional for first message)",
    )


class ChatHistoryRequest(SQLModel):
    thread_id: UUID | None = Field(
        default=None,
        description="Thread ID for the conversation",
    )


class ChatHistory(SQLModel):
    thread_id: UUID | None = Field(
        default=None,
        description="Thread ID for the conversation",
    )
    messages: list[Message] = Field(
        description="List of messages in the chat history",
    )


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)
