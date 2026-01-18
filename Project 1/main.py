from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from schemas import UserResponse, UserCreate, ActionCreate, ActionResponse
from deps import get_db
from models import User, IdempotencyKey, Action
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

# @app.delete("/users/{user_id}/{idempotency_key}")
# def delete_user(user_id: int, idempotency_key: str, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.id == user_id).first()

#     if not user:
#         raise HTTPException(status_code=404, detail="User does not exists.")
    
#     idem_key = db.query(IdempotencyKey).filter((IdempotencyKey.key == idempotency_key)).first()

#     if not idem_key:
#         idem_obj = IdempotencyKey(key=idempotency_key, user_id=user.id, action_id=1)
#         db.add(idem_obj)


#     user.is_deleted = True 

#     return {"message": "User has been deleted"}

@app.post("/actions/{user_id}/{idem_key}")
def create_action(user_id: int, idem_key: str, db: Session = Depends(get_db)) -> ActionResponse:
    db_idem_key = db.query(IdempotencyKey).filter((IdempotencyKey.key == idem_key) & (IdempotencyKey.user_id==user_id)).first()

    if db_idem_key:
        action_id = db_idem_key.action_id
        db_action = db.query(Action).filter(Action.id == action_id).first()

        return ActionResponse(id=db_action.id, status=db_action.status)


    db_action = Action(user_id=user_id, status="Pending")

    db.add(db_action)

    db.flush()

    db_idem_key = IdempotencyKey(key = idem_key, action_id=db_action.id, user_id=user_id)
    db.add(db_idem_key)

    try:
        db.commit()
    except:
        db.rollback()
        raise HTTPException(status_code=500, detail="Action cannot be completed.")

    db.refresh(db_action)
    db.refresh(db_idem_key)
    
    return ActionResponse(id=db_action.id, status=db_action.status)

    