#!/usr/bin/env python3
"""Base module for all other modules in the project."""

#
# Copyright
# Jacob Achira Obara
# 2023
#

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column
)

from sqlalchemy import (
    Integer
)


class Base(DeclarativeBase):
    """Base class for all models in the project.

    Args:
        DeclarativeBase (class): SQLAlchemy declarative base class
    """

    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Representation
    def __repr__(self) -> str:
        return super().__repr__()
