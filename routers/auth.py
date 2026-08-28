# routers/auth.py
from database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from models.user import UserModel
from pydantic import BaseModel, EmailStr
from schemas.token import Token
from security import create_access_token, verify_password
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=["Authentication"])


# Schema for JSON login requests
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/login", response_model=Token)
def login_for_access_token(
    login_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """OAuth2 compatible token login, used by Swagger UI (/docs) Authorize button.

    Note: Swagger passes the email inside login_data.username.
    """
    user = (
        db.query(UserModel)
        .filter(UserModel.email == login_data.username)
        .first()
    )

    if not user or not verify_password(
        login_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login/json", response_model=Token)
def login_json(
    credentials: LoginRequest,
    db: Session = Depends(get_db),
):
    """Standard JSON body login route for web and mobile frontends."""
    user = (
        db.query(UserModel)
        .filter(UserModel.email == credentials.email)
        .first()
    )

    if not user or not verify_password(
        credentials.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}