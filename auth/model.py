import enum
from typing import List
from uuid import UUID

from sqlalchemy import ARRAY, String
from db_config import db
from sqlalchemy.orm import Mapped, mapped_column


class Role(enum.Enum):
    COURIER = "COURIER"
    CONSUMER = "CONSUMER"
    SELLER = "SELLER"
    DEFAULT = "DEFAULT"


class AuthModel(db.Model):
    __tablename__ = "auth"

    identity_id: Mapped[UUID] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(primary_key=True)
    password: Mapped[str] = mapped_column()
    is_operational: Mapped[bool] = mapped_column(default=False)
    roles: Mapped[List[str]] = mapped_column(ARRAY(String), default=[])

    def __init__(
        self, email: str, password: str, identity_id: UUID, roles: List[Role] = []
    ) -> None:
        self.email = email
        self.password = password
        self.identity_id = identity_id
        self.roles = roles
