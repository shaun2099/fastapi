from turtle import title
from fastapi import Body, Depends, FastAPI, Response, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(model: schemas.UserCreate, db: Session = Depends(get_db)):
    # hash the password
    hashed_password = utils.hash_pwd(model.password)
    model.password = hashed_password
    new_user = models.User(**model.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



@router.get('/{user_id}', response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User not found for id: {user_id}")
    return user
