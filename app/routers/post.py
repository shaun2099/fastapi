from fastapi import Body, Depends, FastAPI, Response, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get('/{post_id}', response_model=schemas.PostResponse)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        # response.status_code = 404
        raise HTTPException(status_code=404, detail=f"Post not found for id: {post_id}")
    return post


@router.get('/', response_model=List[schemas.PostResponse])
async def get_posts(db: Session = Depends(get_db), limit: int = 10, search: Optional[str] = ""):
    posts = db.query(models.Post).filter(models.Post .title.contains(search)).limit(limit).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def create_post(model: schemas.PostCreate, db: Session = Depends(get_db),
                      current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    print(model.dict())
    print(vars(current_user))

    new_post = models.Post(owner_id=current_user.id, **model.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.put("/{post_id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
async def update_post(post_id: int, post: schemas.PostCreate, db: Session = Depends(get_db),
                      current_user: schemas.TokenData = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    updated_post = post_query.first()
    if updated_post is None:
        raise HTTPException(status_code=404, detail=f"Post not found for id: {post_id}")

    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to perform requested action")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: Session = Depends(get_db),
                      current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail=f"Post not found for id: {post_id}")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to perform requested action")

    # return {"message": "Post deleted"}
    # post.delete(synchronize_session=False)
    db.delete(post)
    db.commit()
    return Response(status_code=204)
