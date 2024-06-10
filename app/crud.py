# app/crud.py
from sqlalchemy.orm import Session
from app import models, schemas
from typing import Optional, List

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        for key, value in user.dict().items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return {"message": "User deleted successfully"}
    return {"message": "User not found"}

def get_users_list(db: Session, user_name: Optional[str] = None, user_email: Optional[str] = None, user_quotes: Optional[str] = None, user_alphabets: Optional[str] = None):
    query = db.query(models.User)
    if user_name:
        query = query.filter(models.User.name == user_name)
    if user_email:
        query = query.filter(models.User.email == user_email)
    if user_quotes:
        query = query.filter(models.User.quotes == user_quotes)
    if user_alphabets:
        query = query.filter(models.User.name.ilike(f"{user_alphabets}%"))
    return query.all()

def update_user_quotes(db: Session, user_id: int, new_quote: str):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db_user.quotes = new_quote
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user_quotes(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db_user.quotes = None
        db.commit()
        db.refresh(db_user)
    return db_user
