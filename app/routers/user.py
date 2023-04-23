from fastapi import status, HTTPException, Depends, APIRouter, Response
from .. import model, schemas, utils,email
from sqlalchemy.orm import Session
from ..data_base import get_db


router = APIRouter(
    prefix="/user",
    tags=['Users']
)

@router.post("/", status_code= status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user :  schemas.create_user, db: Session = Depends(get_db)):
    user_query = db.query(model.User).filter(model.User.email == user.email)
    email_found = user_query.first()
    if email_found:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"user with email is already  exist")
    else:
        hashed_password = utils.hash(user.password)
        user.password = hashed_password
        user.dict()

        #verifing otp
        if not utils.verify_otp(user.email, user.otp):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP")
        new_user = model.User(user_name=user.user_name, email=user.email, password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

@router.post("/verified",status_code=status.HTTP_202_ACCEPTED)
def verify(user: schemas.verify,db: Session = Depends(get_db)):
    otp = utils.generate_otp()
    email.send_email(user.email, otp)
    utils.save_otp(user.email, otp)
    return {"message":"otp has been sent to your email."}


@router.get("/{id}",response_model=schemas.OutUser)
def get_user(id: int, db: Session = Depends(get_db)):
    request_user =db.query(model.User).filter(model.User.id == id).first()
    if not request_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id:{id} not found")

    return request_user

