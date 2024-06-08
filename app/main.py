from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas, crud
from app.database import SessionLocal, engine
import logging
import logging.config
import os

# Ensure logging.conf is correctly referenced
logging.config.fileConfig(os.path.join(os.path.dirname(__file__), 'logging.conf'), disable_existing_loggers=False)
logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating user: {user.email}")
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        logger.error(f"Email already registered: {user.email}")
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching user by id: {user_id}")
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        logger.error(f"User not found: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    logger.info(f"Updating user: {user_id}")
    return crud.update_user(db=db, user_id=user_id, user=user)

@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    logger.info(f"Deleting user: {user_id}")
    db_user = crud.delete_user(db=db, user_id=user_id)
    if db_user is None:
        logger.error(f"User not found: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/users/", response_model=List[schemas.User])
def read_users(
    skip: int = 0, 
    limit: int = 10, 
    sort_by: str = Query("id", enum=["id", "name", "email", "quotes"]),
    sort_order: str = Query("asc", enum=["asc", "desc"]),
    db: Session = Depends(get_db)
):
    logger.info(f"Fetching users with skip={skip}, limit={limit}, sort_by={sort_by}, sort_order={sort_order}")
    users = crud.get_users(db, skip=skip, limit=limit, sort_by=sort_by, sort_order=sort_order)
    return users

@app.get("/users/filter/", response_model=List[schemas.User])
def filter_users(
    name: Optional[str] = None,
    quote: Optional[str] = None,
    alphabet: Optional[str] = None,
    sort_by: str = Query("id", enum=["id", "name", "email", "quotes"]),
    sort_order: str = Query("asc", enum=["asc", "desc"]),
    db: Session = Depends(get_db)
):
    logger.info(f"Filtering users by name={name}, quote={quote}, alphabet={alphabet}, sort_by={sort_by}, sort_order={sort_order}")
    users = crud.filter_users(db, name=name, quote=quote, alphabet=alphabet, sort_by=sort_by, sort_order=sort_order)
    return users
