from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import get_db, Session
from .. import schemas, models, utils, oauth2

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post('/login', status_code=status.HTTP_200_OK, response_model=schemas.Token)
def login(user_cred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_cred.username).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    if not utils.verify_pwd(user_cred.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    # create a token
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    token = schemas.Token(access_token=access_token, token_type="bearer")
    return token
    # return {'access_token': access_token, "token_type": "bearer"}
