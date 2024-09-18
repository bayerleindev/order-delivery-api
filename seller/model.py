from uuid import uuid4, UUID
from db_config import db
from sqlalchemy.orm import Mapped, mapped_column


class SellerModel(db.Model):
    __tablename__ = "seller"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    document: Mapped[str] = mapped_column(unique=True, index=True)
    name: Mapped[str] = mapped_column()
    latitude: Mapped[float] = mapped_column(nullable=True)
    longitude: Mapped[float] = mapped_column(nullable=True)

    def __init__(
        self, document: str, name: str, latitude: float, longitude: float
    ) -> None:
        self.name = name
        self.document = document
        self.id = uuid4()
        self.latitude = latitude
        self.longitude = longitude

    def to_json(self):
        return {
            "id": str(self.id),
            "document": self.document,
            "name": self.name,
            "latitude": self.latitude,
            "longitude": self.longitude,
        }
