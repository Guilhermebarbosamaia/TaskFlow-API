from typing import List
from database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from models.user import UserModel
from schemas.user import User, UserCreate
from security import get_current_user, hash_password
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["Users"])


def require_admin(current_user: UserModel = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user


@router.get("/admin/users", response_model=List[User])
def get_all_users(
    admin: UserModel = Depends(require_admin), db: Session = Depends(get_db)
):
    return db.query(UserModel).all()


@router.post("", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = (
        db.query(UserModel).filter(UserModel.email == user_data.email).first()
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    user_dict = user_data.model_dump()
    raw_password = user_dict.pop("password")

    new_user = UserModel(
        **user_dict,
        hashed_password=hash_password(raw_password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )
    return user