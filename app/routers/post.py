from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import model, schemas, oauth2
from sqlalchemy.orm import Session
from sqlalchemy import func, case, and_, or_
from ..data_base import get_db
from typing import List, Optional
from sqlalchemy.sql.expression import exists

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)
#@router.get("/", response_model= List[schemas.Post])

@router.get("/", response_model= List[schemas.VoteOut])
def get_post(db: Session = Depends(get_db), search: Optional[str] = "", user_id: int = Depends(oauth2.get_current_user)):
    current_user = int(user_id.id)
    subq = db.query(model.Vote).filter(model.Vote.user_id == current_user, model.Vote.post_id == model.Post.id).subquery()
    posts =  db.query(model.Post, func.count(model.Vote.post_id).label("votes"),
                      exists().where(and_(subq.c.post_id == model.Post.id,
                                          subq.c.user_id == current_user)).label("voted"))\
        .join(model.Vote, model.Vote.post_id == model.Post.id, isouter=True).group_by(model.Post.id)\
        .filter(model.Post.title.contains(search)).all()

    return posts
@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.CreatePost,)
def create_post(post : schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):

    post.dict()
    new_post = model.Post(owner_id = user_id.id, **post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model= schemas.VoteOut)
def get_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    current_user = int(user_id.id)
    subq = db.query(model.Vote).filter(model.Vote.user_id == current_user,
                                       model.Vote.post_id == model.Post.id).subquery()
    posts = db.query(model.Post, func.count(model.Vote.post_id).label("votes"),
                     exists().where(and_(subq.c.post_id == model.Post.id,
                                         subq.c.user_id == current_user)).label("voted")) \
        .join(model.Vote, model.Vote.post_id == model.Post.id, isouter=True).group_by(model.Post.id) \
        .filter(model.Post.id == id).first()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} not found")

    return posts

@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):

    post_query = db.query(model.Post).filter(model.Post.id == id)
    deleted_posts = post_query.first()
    owner_id = str(deleted_posts.owner_id)
    if deleted_posts == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")

    if owner_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"not authorized to perform requested action")

    post_query.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model= schemas.Post)
def update_post(id: int, post : schemas.PostBase, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    post_query = db.query(model.Post).filter(model.Post.id == id)
    updated_post = post_query.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    owner_id = str(updated_post.owner_id)
    if owner_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return updated_post