from sqlalchemy.orm import Session
from . import models, schemas, security

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

import uuid

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_post(db: Session, post_id: uuid.UUID):
    return db.query(models.Post).filter(models.Post.id == post_id).first()

def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Post).offset(skip).limit(limit).all()

def create_user_post(db: Session, post: schemas.PostCreate, user_id: uuid.UUID):
    db_post = models.Post(**post.model_dump(), author_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def update_post(db: Session, post: models.Post, post_update: schemas.PostUpdate):
    update_data = post_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(post, key, value)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

def delete_post(db: Session, post: models.Post):
    db.delete(post)
    db.commit()
    return post