#!/usr/bin/env python3
"""Health model.
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
from datetime import datetime


class Heat(Base):
    """Health Articles class. Manages health_articles table

    Args:
        Base (Inherited class): Base class
    """

    # Table name
    __tablename__ = 'heats'

    # Columns
    title: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
    content: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
    )
    published_date: Mapped[datetime] = mapped_column(
        nullable=False,
        default=datetime.utcnow()
    )

    # Foreign keys
    author_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'),
        nullable=False
    )

    # Relationships
    author = relationship('User', back_populates='heats')
    heat_comments = relationship('HeatComment', back_populates='heat')

    def __repr__(self) -> str:
        """String representation of the class.

        Returns:
            str: String representation of the class
        """
        def rep():
            id = f"(ID {self.id!r}) -> "
            title = f"<Heat {self.title!r}> "
            content = f"((Content={self.content!r}) "
            p_date = f"(Added_date={self.published_date!r}) "
            author_id = f"(Author_ID={self.author_id!r}) "
            author = f"(Author={self.author!r}) "
            comments = f"(Comments={self.heat_comments!r})) "

            return (
                id + title + content + p_date + author_id + author + comments
            )
        return rep()


# Declare Health comments class
class HeatComment(Base):
    """Health comments class. Manages health_comments table

    Args:
        Base (Inherited class): Base class
    """

    # Table name
    __tablename__ = 'heat_comments'

    # Columns
    comment: Mapped[str] = mapped_column(
        String(1000),
        nullable=False
    )
    comment_date: Mapped[datetime] = mapped_column(
        nullable=False,
        default=datetime.utcnow()
    )

    # Foreign keys
    author_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'),
        nullable=False
    )
    heat_id: Mapped[int] = mapped_column(
        ForeignKey('heats.id'),
        nullable=False
    )

    # Relationships
    author = relationship('User', back_populates='heat_comments')
    heat = relationship('Heat', back_populates='heat_comments')

    def __repr__(self) -> str:
        """String representation of the class.

        Returns:
            str: String representation of the class
        """
        def rep():
            comm = f"<HeatComment {self.comment!r}> "
            date = f"((Date={self.comment_date!r}) "
            author = f"(Author={self.author!r}) "
            heat = f"(Heat={self.heat!r})) "

            return (
                comm + date + author + heat
            )

        return rep()
