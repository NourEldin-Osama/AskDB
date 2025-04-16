import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import col, func, select

from app.api.dependencies import CurrentUser, SessionDependency
from app.models import Response, Thread, ThreadCreate, ThreadPublic, ThreadsPublic, ThreadUpdate

router = APIRouter(prefix="/threads", tags=["threads"])


@router.get("/", response_model=ThreadsPublic)
def read_threads(session: SessionDependency, current_user: CurrentUser, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve threads.
    """

    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Thread)
        count = session.exec(count_statement).one()
        statement = select(Thread).order_by(col(Thread.created_at).desc()).offset(skip).limit(limit)
        threads = session.exec(statement).all()
    else:
        count_statement = select(func.count()).select_from(Thread).where(Thread.user_id == current_user.id)
        count = session.exec(count_statement).one()
        statement = (
            select(Thread)
            .where(Thread.user_id == current_user.id)
            .order_by(col(Thread.created_at).desc())
            .offset(skip)
            .limit(limit)
        )
        threads = session.exec(statement).all()

    return ThreadsPublic(data=threads, count=count)


@router.get("/{id}", response_model=ThreadPublic)
def read_thread(session: SessionDependency, current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Get thread by ID.
    """
    thread = session.get(Thread, id)
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    if not current_user.is_superuser and (thread.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return thread


@router.post("/", response_model=ThreadPublic)
def create_thread(*, session: SessionDependency, current_user: CurrentUser, thread_in: ThreadCreate) -> Any:
    """
    Create new thread.
    """
    thread = Thread.model_validate(thread_in, update={"user_id": current_user.id})
    session.add(thread)
    session.commit()
    session.refresh(thread)
    return thread


@router.put("/{id}", response_model=ThreadPublic)
def update_thread(
    *,
    session: SessionDependency,
    current_user: CurrentUser,
    id: uuid.UUID,
    thread_in: ThreadUpdate,
) -> Any:
    """
    Update an thread.
    """
    thread = session.get(Thread, id)
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    if not current_user.is_superuser and (thread.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    update_dict = thread_in.model_dump(exclude_unset=True)
    thread.sqlmodel_update(update_dict)
    session.add(thread)
    session.commit()
    session.refresh(thread)
    return thread


@router.delete("/{id}")
def delete_thread(session: SessionDependency, current_user: CurrentUser, id: uuid.UUID) -> Response:
    """
    Delete an thread.
    """
    thread = session.get(Thread, id)
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    if not current_user.is_superuser and (thread.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    session.delete(thread)
    session.commit()
    return Response(message="Thread deleted successfully")
