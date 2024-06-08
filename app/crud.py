from sqlalchemy.orm import Session
from app import models, schemas
from sqlalchemy import asc, desc, or_

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = user.password  # Hashing should be done here
    db_user = models.User(
        name=user.name, email=user.email, quotes=user.quotes, hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        for var, value in vars(user).items():
            setattr(db_user, var, value) if value else None
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()

def get_users(db: Session, skip: int = 0, limit: int = 10, sort_by: str = "id", sort_order: str = "asc"):
    sort_column = getattr(models.User, sort_by, None)
    if sort_column is None:
        sort_column = models.User.id
    order_by = asc(sort_column) if sort_order == "asc" else desc(sort_column)
    return db.query(models.User).order_by(order_by).offset(skip).limit(limit).all()

def filter_users(db: Session, name: str = None, quote: str = None, alphabet: str = None, sort_by: str = "id", sort_order: str = "asc"):
    query = db.query(models.User)
    if name:
        query = query.filter(models.User.name.ilike(f"%{name}%"))
    if quote:
        query = query.filter(models.User.quotes.ilike(f"%{quote}%"))
    if alphabet:
        query = query.filter(models.User.name.ilike(f"{alphabet}%"))
    sort_column = getattr(models.User, sort_by, None)
    if sort_column is None:
        sort_column = models.User.id
    order_by = asc(sort_column) if sort_order == "asc" else desc(sort_column)
    return query.order_by(order_by).all()
