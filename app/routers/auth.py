from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import model, schemas, utils, oauth2
from sqlalchemy.orm import Session
from ..data_base import get_db

router = APIRouter(tags=['login'])


@router.post('/login' ,response_model=schemas.Token)
def login(user_credential: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.email == user_credential.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'InvalidCredential')

    if not utils.verify(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'InvalidCredential')
    access_token = oauth2.create_access_token(data= {'user_id': user.id})
    return{'access_token':access_token, 'token_type': 'bearer'}