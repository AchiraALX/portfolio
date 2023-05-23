#!/usr/bin/env python3
"""GitHub model
"""

from models.base import Base
from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import (
    relationship,
    Mapped,
    mapped_column
)
from typing import Optional
from datetime import datetime


# Declare Ghub class
class Ghub(Base):
    """Ghub class

    Args:
        Base (_type_): Base class model
    """

    # Table name
    __tablename__ = 'ghub'

    # Columns
    repos_num: Mapped[int] = mapped_column(nullable=False)
    repos: Mapped[str] = mapped_column(nullable=False)
    followers: Mapped[int] = mapped_column(nullable=False)
    stars: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(1000))
    last_refreshed: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow()
    )

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
