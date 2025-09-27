from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List
import uuid

from . import crud, models, schemas, security
from .database import SessionLocal, engine, get_db
from .integrations.tistory import TistoryAdapter
from .integrations.velog import VelogAdapter
from .integrations.base import BlogAdapter

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=schemas.User)
def read_users_me(current_user: schemas.User = Depends(security.get_current_user)):
    return current_user

@app.post("/posts/", response_model=schemas.Post)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(security.get_current_user),
):
    return crud.create_user_post(db=db, post=post, user_id=current_user.id)


@app.get("/posts/", response_model=List[schemas.Post])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = crud.get_posts(db, skip=skip, limit=limit)
    return posts


@app.get("/posts/{post_id}", response_model=schemas.Post)
def read_post(post_id: uuid.UUID, db: Session = Depends(get_db)):
    db_post = crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@app.put("/posts/{post_id}", response_model=schemas.Post)
def update_post(
    post_id: uuid.UUID,
    post_update: schemas.PostUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(security.get_current_user),
):
    db_post = crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this post")
    return crud.update_post(db=db, post=db_post, post_update=post_update)


@app.delete("/posts/{post_id}", response_model=schemas.Post)
def delete_post(
    post_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(security.get_current_user),
):
    db_post = crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    return crud.delete_post(db=db, post=db_post)


def get_blog_adapter(platform: str) -> BlogAdapter:
    if platform == "tistory":
        return TistoryAdapter()
    elif platform == "velog":
        return VelogAdapter()
    else:
        raise HTTPException(status_code=400, detail="Unsupported blog platform")


@app.post("/posts/{post_id}/publish", response_model=dict)
def publish_post(
    post_id: uuid.UUID,
    publish_data: schemas.BlogPublish,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(security.get_current_user),
):
    db_post = crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to publish this post")

    adapter = get_blog_adapter(publish_data.platform)
    # In a real app, you'd pass real credentials
    adapter.authenticate(credentials={})

    post_data = schemas.PostCreate(title=db_post.title, content=db_post.content)

    try:
        url = adapter.create_post(post_data)
        return {"message": f"Post published to {publish_data.platform} at {url}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def read_root():
    return {"Hello": "World"}