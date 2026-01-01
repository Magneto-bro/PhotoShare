from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.entity.models import Comment
from src.schemas.comments import CommentCreate, CommentUpdate, CommentResponse

router = APIRouter(prefix="/comments", tags=["comments"])

@router.post("/", response_model=CommentResponse)
def create_comment(comment: CommentCreate, db: Session = Depends(get_db), user_id: int = 1):
    new_comment = Comment(
        content=comment.text,
        photo_id=comment.photo_id,
        user_id=user_id
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

@router.put("/{comment_id}", response_model=CommentResponse)
def update_comment(comment_id: int, comment: CommentUpdate, db: Session = Depends(get_db), user_id: int = 1):
    db_comment = db.query(Comment).filter(
        Comment.id == comment_id,
        Comment.user_id == user_id
    ).first()

    if not db_comment:
        raise HTTPException(status_code=404, detail="Коментар не знайдено або він не належить користувачу")

    db_comment.content = comment.text
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.delete("/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db), role: str = "user"):
    if role not in ["moderator", "admin"]:
        raise HTTPException(status_code=403, detail="Недостатньо прав для видалення коментаря")

    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not db_comment:
        raise HTTPException(status_code=404, detail="Коментар не знайдено")

    db.delete(db_comment)
    db.commit()
    return {"detail": "Коментар успішно видалено"}