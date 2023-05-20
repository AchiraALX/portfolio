#!/usr/bin/env python3
"""Repositories model"""

from models.base import Base

from sqlalchemy import (
    ForeignKey
)

from sqlalchemy.orm import (
    relationship,
    Mapped,
    mapped_column
)
from typing import Optional


# Declare Repo class
class Repo(Base):
    """Repositories class

    Args:
        Base (class): Base class
    """

    # Table name
    __tablename__ = 'repos'

    # Columns
    repository_name: Mapped[str] = mapped_column(
        nullable=False
    )

    repository_url: Mapped[str] = mapped_column(
        nullable=False
    )

    repository_description: Mapped[Optional[str]]

    # Foreign keys
    owner_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'),
        nullable=False
    )

    # Relationships
    author_id = relationship(
        'User',
        back_populates='repos'
    )

    # Representation
    def __repr__(self) -> str:
        return \
            f'<Repo {self.id}> \
            user_id={self.author_id} \
            name={self.repository_name} \
            url={self.repository_url} \
            description={self.repository_description}'
