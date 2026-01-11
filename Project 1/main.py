from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from schemas import UserResponse, UserCreate
from deps import get_db
from models import User
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session=Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    return user

@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="User already exists")
    
    db.refresh(db_user)
    
    return db_user


    