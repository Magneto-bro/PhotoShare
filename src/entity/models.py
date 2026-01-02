from enum import Enum
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship



class Base(DeclarativeBase):
    pass


class RoleEnum(str, Enum):
    user = "user"
    moderator = "moderator"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    refresh_token: Mapped[str | None] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    confirmed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    role: Mapped[RoleEnum] = mapped_column(SQLEnum(RoleEnum, name="role_enum"), default=RoleEnum.user, nullable=False)

    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="author", cascade="all, delete-orphan")

    is_active: Mapped[bool] = mapped_column(Boolean, default = True)
    is_banned: Mapped[bool]=mapped_column(Boolean, default = False)

    photos: Mapped[list["Photo"]] = relationship(
        "Photo",
        back_populates="owner",
        cascade="all, delete-orphan"
    )
    
    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="author",
        cascade="all, delete-orphan"
    )


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    photo_id: Mapped[int] = mapped_column(ForeignKey("photos.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    photo: Mapped["Photo"] = relationship("Photo", back_populates="comments")
    author: Mapped["User"] = relationship("User", back_populates="comments")
    
    
photo_tags_table = Table(
    "photo_tags",
    Base.metadata,
    mapped_column("photo_id", ForeignKey("photos.id", ondelete="CASCADE"), primary_key=True),
    mapped_column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)
)
    
    
class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    photos = relationship("Photo", secondary=photo_tags_table, back_populates="tags")
    

class Photo(Base):
    __tablename__ = "photos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    tags = relationship("Tag", secondary=photo_tags_table, back_populates="photos")
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    owner: Mapped["User"] = relationship("User", back_populates="photos")


    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    tags: Mapped[list["Tag"]] = relationship(
        "Tag",
        secondary=photo_tags_table,
        back_populates="photos"
    )

    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="photo",
        cascade="all, delete-orphan"
    )