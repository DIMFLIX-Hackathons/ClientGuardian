import enum
import secrets
import string
from datetime import datetime
from typing import Any

from sqlalchemy import (
    BIGINT,
    TIMESTAMP,
    Boolean,
    Column,
    Enum,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from .db_manager import Base

characters = string.ascii_letters + string.digits


class TaskStatus(enum.Enum):
    error = "error"
    expectation = "expectation"
    completed = "completed"


class Token(Base):
    __tablename__ = "tokens"
    id = Column(BIGINT, primary_key=True)
    token = Column(
        String,
        nullable=False,
        default="".join(secrets.choice(characters) for _ in range(32)),
    )
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now)
    lifetime = Column(TIMESTAMP, nullable=False, default=datetime.now)
    enabled = Column(Boolean, nullable=False, default=True)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "balance": self.balance,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class Task(Base):
    __tablename__ = "tasks"
    id = Column(BIGINT, primary_key=True)
    token_id = Column(BIGINT, ForeignKey("tokens.id"), nullable=False)
    original_path = Column(String, nullable=False)
    results_path = Column(String, nullable=True)
    status = Column(Integer, nullable=False, default=0) # 0 - expectation, 1 - completed, 2 - error 
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now)

    token = relationship("Token", backref="tasks")
