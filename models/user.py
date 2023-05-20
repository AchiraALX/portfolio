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
        nullable=False
    )
    password: Mapped[str] = mapped_column(
        String(50),
        nullable=False
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
    blogs: Mapped[List[str]] = relationship(
        'Blog',
        back_populates='author'
    )
    heats: Mapped[List[str]] = relationship(
        'Heat', back_populates='author'
    )
    blog_comments: Mapped[List[str]] = relationship(
        'BlogComment',
        back_populates='author'
    )
    heat_comments: Mapped[List[str]] = relationship(
        'HeatComment',
        back_populates='author'
    )
    tasks: Mapped[List[str]] = relationship(
        'Task',
        back_populates='task_assignee'
    )
    task_comments: Mapped[List[str]] = relationship(
        'TaskComment',
        back_populates='author'
    )
    repos: Mapped[List[str]] = relationship(
        'Repo',
        back_populates='author_id'
    )
    ghub: Mapped[List[str]] = relationship(
        'Ghub',
        back_populates='owner_info'
    )

    # Representation
    def __repr__(self) -> str:
        return \
            f'<User {self.id}> \
            username={self.username} \
            email={self.email} \
            name={self.name}'
