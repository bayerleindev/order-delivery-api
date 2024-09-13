from uuid import uuid4, UUID
from db_config import db
from sqlalchemy.orm import Mapped, mapped_column


class ConsumerModel(db.Model):
    __tablename__ = "consumer"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    document: Mapped[str] = mapped_column(unique=True, index=True)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True, nullable=True)
    phone: Mapped[str] = mapped_column(nullable=True)

    def __init__(self, document: str, name: str, email: str, phone: str) -> None:
        self.name = name
        self.document = document
        self.email = email
        self.phone = phone
        self.id = uuid4()

    def to_json(self):
        return {
            "id": str(self.id),
            "document": self.document,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
        }
