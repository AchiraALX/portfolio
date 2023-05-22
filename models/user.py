#!/usr/bin/env python3
"""User module."""

from datetime import datetime
from models.base import Base
from sqlalchemy import String, DateTime
from sqlalchemy.orm import (
    relationship,
    Mapped,
    mapped_column
)
from typing import List, Optional
from .blog import Blog, BlogComment
from .heat import Heat, HeatComment
from .task import Task, TaskComment
from .repo import Repo
from .ghub import Ghub


# Declare User class
class User(Base):
    """The User class.

    Args:
        Base (Inherited class): Base class
    """

    # Table name
    __tablename__ = 'users'

    # Columns
    username: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True
    )
    email: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True
    )
    password: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True
    )
    name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=False
    )
    gender: Mapped[str] = mapped_column(
        String(5),
        nullable=False
    )
    reg_date: Mapped[DateTime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow()
    )
    last_login: Mapped[DateTime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow()
    )

    # Relationships
    blogs = relationship(
        Blog,
        back_populates='author',
        uselist=True
    )
    heats = relationship(
        Heat, back_populates='author', uselist=True
    )
    blog_comments = relationship(
        BlogComment,
        back_populates='author',
        uselist=True
    )
    heat_comments = relationship(
        HeatComment,
        back_populates='author',
        uselist=True
    )
    tasks = relationship(
        Task,
        back_populates='task_assignee',
        uselist=True
    )
    task_comments = relationship(
        TaskComment,
        back_populates='author',
        uselist=True
    )
    repos = relationship(
        Repo,
        back_populates='author_id',
        uselist=True
    )
    ghub = relationship(
        Ghub,
        back_populates='owner_info',
        uselist=True
    )

    # Representation
    def __repr__(self) -> str:
        return \
            f'<User {self.id}> \
            username={self.username} \
            email={self.email} \
            name={self.name}'
