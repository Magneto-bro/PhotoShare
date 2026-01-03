from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.database.db import get_db
from src.entity.models import Comment
from src.schemas.comments import CommentCreate, CommentUpdate, CommentResponse

router = APIRouter(prefix="/comments", tags=["comments"])

@router.post("/", response_model=CommentResponse)
async def create_comment(comment: CommentCreate, db: AsyncSession = Depends(get_db), user_id: int = 1):
    new_comment = Comment(
        content=comment.text,
        photo_id=comment.photo_id,
        user_id=user_id
    )
    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)
    return new_comment

@router.get("/", response_model=list[CommentResponse])
async def get_comments(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Comment))
    return result.scalars().all()

@router.get("/{comment_id}", response_model=CommentResponse)
async def get_comment(comment_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Comment).filter(Comment.id == comment_id))
    db_comment = result.scalar_one_or_none()
    if not db_comment:
        raise HTTPException(status_code=404, detail="Коментар не знайдено")
    return db_comment

@router.put("/{comment_id}", response_model=CommentResponse)
async def update_comment(comment_id: int, comment: CommentUpdate, db: AsyncSession = Depends(get_db), user_id: int = 1):
    result = await db.execute(
        select(Comment).filter(Comment.id == comment_id, Comment.user_id == user_id)
    )
    db_comment = result.scalar_one_or_none()
    if not db_comment:
        raise HTTPException(status_code=404, detail="Коментар не знайдено або він не належить користувачу")

    db_comment.content = comment.text
    await db.commit()
    await db.refresh(db_comment)
    return db_comment

@router.delete("/{comment_id}")
async def delete_comment(comment_id: int, db: AsyncSession = Depends(get_db), role: str = "user"):
    if role not in ["moderator", "admin"]:
        raise HTTPException(status_code=403, detail="Недостатньо прав для видалення коментаря")

    result = await db.execute(select(Comment).filter(Comment.id == comment_id))
    db_comment = result.scalar_one_or_none()
    if not db_comment:
        raise HTTPException(status_code=404, detail="Коментар не знайдено")

    await db.delete(db_comment)
    await db.commit()
    return {"detail": "Коментар успішно видалено"}