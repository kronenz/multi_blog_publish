from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from uuid import UUID
from backend.src.models.user import User, UserCreate
from backend.src.services.user_service import UserService
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()
user_service = UserService()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/token")
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> dict[str, str]:
    user = user_service.get_user_by_email(form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": user.email, "exp": datetime.utcnow() + access_token_expires}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": encoded_jwt, "token_type": "bearer"}

@router.post("/users", response_model=User, status_code=201)
def create_user(user: UserCreate):
    password_hash = pwd_context.hash(user.password)
    new_user = User(name=user.name, email=user.email, password_hash=password_hash)
    return user_service.create_user(new_user)

@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: UUID):
    user = user_service.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
