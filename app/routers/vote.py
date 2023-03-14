from fastapi import status, HTTPException, Depends, APIRouter
from .. import schemas, data_base, model, oauth2
from sqlalchemy.orm import Session
router = APIRouter(
    prefix="/vote",
    tags = ['vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(data_base.get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(model.Post).filter(model.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {vote.post_id}"
                                                                          f" does not found")
    vote_query = db.query(model.Vote).filter(
        model.Vote.post_id == vote.post_id, model.Vote.user_id == current_user.id)

    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        new_vote = model.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"successfully deleted vote"}