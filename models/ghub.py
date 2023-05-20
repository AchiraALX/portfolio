#!/usr/bin/env python3
"""GitHub model
"""

from models.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    relationship,
    Mapped,
    mapped_column
)
from typing import Optional


# Declare Ghub class
class Ghub(Base):
    """Ghub class

    Args:
        Base (_type_): Base class model
    """

    # Table name
    __tablename__ = 'ghub'

    # Columns
    repos: Mapped[int] = mapped_column(nullable=False)
    followers: Mapped[int] = mapped_column(nullable=False)
    stars: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[Optional[str]]

    # Foreign Keys
    owner_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'),
        nullable=False
    )

    # Relationship
    owner_info = relationship(
        'User',
        back_populates='ghub'
    )

    # Representation
    def __repr__(self) -> str:
        return \
            f'<Ghub={self.id}\
            repositories={self.repos}\
            followers={self.followers}\
            stars={self.stars}\
            description={self.description}'
