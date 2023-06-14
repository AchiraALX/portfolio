#!/usr/bin/env python3
"""Token model.
"""

from models.base import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import (
    relationship,
    Mapped,
    mapped_column
)


# Declare Token class
class Token(Base):
    """Token class.

    Args:
        Base (_type_): Base class model
    """

    # Table name
    __tablename__ = 'tokens'

    # Columns
    token: Mapped[str] = mapped_column(
        String(1000),
        nullable=False
    )

    # Foreign Keys
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'),
        nullable=False
    )

    # Relationship
    user_info = relationship(
        'User',
        back_populates='tokens'
    )

    # Representation
    def __repr__(self) -> str:
        return f'<Token={self.id}> {self.token!r}'
