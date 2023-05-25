#!/usr/bin/env python3
"""Blog model
"""

#
# Copyright
# Jacob Achira Obara
# 2023
#

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


# Declare Blog class
class Blog(Base):
    """The Blog class. Manages blogs table

    Args:
        Base (Inherited class): Base class
    """

    # Table name
    __tablename__ = 'blogs'

    # Columns
    blog_title: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
    blog_content: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
    )
    blog_published_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow()
    )
    last_updated_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow()
    )

    # Foreign keys
    author_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'),
        nullable=False
    )

    # Relationships
    blog_comments = relationship('BlogComment', back_populates='blog')
    author = relationship('User', back_populates='blogs')

    def __repr__(self) -> str:
        """String representation of the class.

        Returns:
            str: String representation of the class
        """
        return \
            f'<Blog {self.blog_title!r}>\n\
            author={self.author!r} \n\
            author_id={self.author_id!r}\n\
            added_date={self.blog_published_date!r} \n\
            '


# Declare BlogComment class
class BlogComment(Base):
    """The BlogComment class. Manages blog_comments table

    Args:
        Base (Inherited class): Base class
    """

    # Table name
    __tablename__ = 'blog_comments'

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
    blog_id: Mapped[int] = mapped_column(
        ForeignKey('blogs.id'),
        nullable=False
    )
    author_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'),
        nullable=False
    )

    # Relationships
    blog = relationship('Blog', back_populates='blog_comments')
    author = relationship('User', back_populates='blog_comments')

    def __repr__(self) -> str:
        """String representation of the class.

        Returns:
            str: String representation of the class
        """
        return f'<BlogComment {self.comment} blog={self.blog} author={self.author}>'
