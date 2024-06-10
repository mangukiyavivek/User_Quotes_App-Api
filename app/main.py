# app/main.py
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app import crud, models, schemas
from app.database import SessionLocal, engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    return crud.update_user(db=db, user_id=user_id, user=user)

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return crud.delete_user(db=db, user_id=user_id)

@app.put("/users/{user_id}/quotes", response_model=schemas.User)
def update_user_quotes(user_id: int, new_quote: str, db: Session = Depends(get_db)):
    return crud.update_user_quotes(db=db, user_id=user_id, new_quote=new_quote)

@app.delete("/users/{user_id}/quotes", response_model=schemas.User)
def delete_user_quotes(user_id: int, db: Session = Depends(get_db)):
    return crud.delete_user_quotes(db=db, user_id=user_id)

@app.get("/users/", response_model=List[schemas.User])
def get_users_list(
    db: Session = Depends(get_db),
    user_name: Optional[str] = None,
    user_email: Optional[str] = None,
    user_quotes: Optional[str] = None,
    user_alphabets: Optional[str] = None
):
    return crud.get_users_list(db=db, user_name=user_name, user_email=user_email, user_quotes=user_quotes, user_alphabets=user_alphabets)
