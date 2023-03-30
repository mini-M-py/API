from fastapi import status, HTTPException, Depends, APIRouter, Response
from .. import schemas, data_base, model, oauth2
from sqlalchemy.orm import Session
router = APIRouter(
    prefix="/comments",
    tags = ['comments']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def comment( comment: schemas.Comment, db: Session = Depends(data_base.get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(model.Post).filter(model.Post.id == comment.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {comment.post_id} "
                                                                         f"does not found")

    comment_found = db.query(model.Comment).filter(model.Comment.post_id == comment.post_id,
                                                   model.Comment.user_id == current_user.id).first()
    if comment_found:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"user {current_user.id} has already commented on post {comment.post_id}")
    else:
        new_comment = model.Comment(post_id = comment.post_id, user_id = current_user.id, comments = comment.comment)
        db.add(new_comment)
        db.commit()
    return {'message':'successfully added comment'}

@router.get("/{id}", response_model=list[schemas.CommentOut])
def get_comment(id: int, db: Session = Depends(data_base.get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(model.Post).filter(model.Post.id == id).first()
    if post_query == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    post = db.query(model.Comment).filter(model.Comment.post_id == id).all()
    return post

@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_comment(id: int, db: Session = Depends(data_base.get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(model.Post).filter(model.Post.id == id).first()
    if post_query == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")

    post = db.query(model.Comment).filter(model.Comment.post_id == id, model.Comment.user_id == current_user.id)

    deleted = post.first()

    if deleted == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"you have not commented on post yet")

    owner_id = str(deleted.user_id)

    if owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = f"Not authorized to perform requested action")

    post.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/", response_model=schemas.CommentOut)
def update_comment( comment: schemas.Comment_Update, db: Session =  Depends(data_base.get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(model.Post). filter(model.Post.id == comment.post_id).first()
    if post_query == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")

    post = db.query(model.Comment).filter(model.Comment.post_id == comment.post_id, model.Comment.user_id == current_user.id)

    updated_comment = post.first()
    if updated_comment == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"you have not comment on the post yet!")

    owner_id = str(updated_comment.user_id)

    if owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorize for requested action")

    post.update(comment.dict(), synchronize_session = False)
    db.commit()
    return updated_comment