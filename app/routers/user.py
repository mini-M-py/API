from fastapi import status, HTTPException, Depends, APIRouter
from .. import model, schemas, utils
from sqlalchemy.orm import Session
from ..data_base import get_db


router = APIRouter(
    prefix="/user",
    tags=['Users']
)

@router.post("/", status_code= status.HTTP_201_CREATED, response_model=schemas.user_response)
def create_user(user :  schemas.create_user, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    user.dict()
    new_user = model.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model= schemas.user_response)
def get_user(id: int, db: Session = Depends(get_db)):
    request_user =db.query(model.User).filter(model.User.id == id).first()
    if not request_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id:{id} not found")

    return request_user