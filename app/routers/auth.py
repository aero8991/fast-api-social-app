from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models, utils, oauth2
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import TokenData, Token

router = APIRouter(
    prefix="/login",
    tags=['Authentication']

)

@router.post('/', response_model=Token)
def login(user: OAuth2PasswordRequestForm = Depends() ,db: Session = Depends(get_db)):

    #first find the user youre looking for. Then youve got that user you can acess their other info!
    #Outh2PW converts #username and # password so we have to convert user/email
    username = db.query(models.User).filter(
        models.User.email == user.username).first()
    if not username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    if not utils.verify_password(user.password, username.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    #create a token
    access_token = oauth2.create_access_token(data={"user_id": username.id}) #changed this
    
    #return token
    return {"access_token": access_token, "token_type": "bearer"}





   
    
