from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app import crud
from app.api.dependencies import CurrentUser, SessionDependency
from app.core import security
from app.core.config import settings
from app.core.security import get_password_hash
from app.models import NewPassword, Response, Token, UserPublic
from app.utils import (
    verify_password_reset_token,
)

router = APIRouter(tags=["login"])


@router.post("/login/access-token")
def login_access_token(session: SessionDependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.authenticate(session=session, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(access_token=security.create_access_token(user.id, expires_delta=access_token_expires))


@router.post("/login/test-token", response_model=UserPublic)
def test_token(current_user: CurrentUser) -> Any:
    """
    Test access token
    """
    return current_user


@router.post("/password-recovery/{email}")
def recover_password(email: str, session: SessionDependency) -> Response:
    """
    Password Recovery
    """
    user = crud.get_user_by_email(session=session, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system.",
        )
    return Response(message="Password recovery email sent")


@router.post("/reset-password/")
def reset_password(session: SessionDependency, body: NewPassword) -> Response:
    """
    Reset password
    """
    email = verify_password_reset_token(token=body.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = crud.get_user_by_email(session=session, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system.",
        )
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    hashed_password = get_password_hash(password=body.new_password)
    user.hashed_password = hashed_password
    session.add(user)
    session.commit()
    return Response(message="Password updated successfully")
