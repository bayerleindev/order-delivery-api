from uuid import uuid4, UUID
from db_config import db
from sqlalchemy.orm import Mapped, mapped_column


class SellerModel(db.Model):
    __tablename__ = "seller"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    document: Mapped[str] = mapped_column(unique=True, index=True)
    name: Mapped[str] = mapped_column()

    def __init__(self, document: str, name: str) -> None:
        self.name = name
        self.document = document
        self.id = uuid4()

    def to_json(self):
        return {
            "id": str(self.id),
            "document": self.document,
            "name": self.name,
        }
