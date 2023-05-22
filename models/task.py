#!/usr/bin/env python3
"""Tasks model
"""

from models.base import Base
from sqlalchemy import (
    ForeignKey,
    String,
    DateTime
)
from sqlalchemy.orm import (
    relationship,
    Mapped,
    mapped_column
)
from typing import Optional
from datetime import datetime


# Declare Task class
class Task(Base):
    """Tasks class. Manages tasks table

    Args:
        Base (Inherited class): Base class
    """

    # Table name
    __tablename__ = 'tasks'

    # Columns
    task_title: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    task_description: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
        default='No description'
    )

    task_status: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        default='pending'
    )

    task_due_date: Mapped[datetime] = mapped_column(
        nullable=False
    )

    task_created_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow(),
        nullable=False
    )

    task_last_modified_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow(),
        nullable=False
    )

    # Foreign keys
    assignee_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'),
        nullable=False
    )

    # Relationships
    task_assignee = relationship(
        'User',
        back_populates='tasks'
    )
    task_comments = relationship(
        'TaskComment',
        back_populates='task'
    )

    # Representation
    def __repr__(self) -> str:
        return \
            f'<Task {self.id}> \
            user_id={self.username_id} \
            title={self.task_title} \
            description={self.task_description} \
            status={self.task_status} \
            due_date={self.task_due_date}'


# Declare TaskComment class
class TaskComment(Base):
    """Task comments class. Manages task_comments table

    Args:
        Base (Inherited class): Base class
    """

    # Table name
    __tablename__ = 'task_comments'

    # Columns
    task_comment: Mapped[str] = mapped_column(
        String(1000),
        nullable=False
    )
    task_comment_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow()
    )
    last_modified_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow()
    )

    # Foreign keys
    task_id: Mapped[int] = mapped_column(
        ForeignKey('tasks.id'),
        nullable=False
    )

    author_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'),
        nullable=False
    )

    # Relationships
    task = relationship(
        'Task',
        back_populates='task_comments'
    )

    author = relationship(
        'User',
        back_populates='task_comments'
    )

    # Representation
    def __repr__(self) -> str:
        return \
            f'<TaskComment {self.id}> \
            task_id={self.task_id} \
            author_id={self.author_id} \
            comment={self.task_comment}'
