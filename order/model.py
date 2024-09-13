from datetime import datetime
from typing import List
from uuid import UUID
from sqlalchemy.orm import relationship
from consumer.model import ConsumerModel
from db_config import db
from sqlalchemy import Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from seller.model import SellerModel


class OrderModel(db.Model):
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    number: Mapped[str] = mapped_column(unique=True, index=True)
    status: Mapped[str] = mapped_column()
    seller_id: Mapped[UUID] = mapped_column(ForeignKey(SellerModel.id), index=True)
    consumer_id: Mapped[UUID] = mapped_column(ForeignKey(ConsumerModel.id), index=True)
    created_at: Mapped[datetime] = mapped_column(nullable=True, default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(nullable=True, default=None)
    seller = relationship("SellerModel")
    consumer = relationship("ConsumerModel")

    address = None
    items: List = []

    def __init__(
        self, number: str, status: str, seller_id: UUID, consumer_id: UUID
    ) -> None:
        self.number = number
        self.status = status
        self.seller_id = seller_id
        self.consumer_id = consumer_id

    def is_finalized(self):
        return self.status in ["DELIVERED", "CANCELLED"]

    def to_json(self):
        return {
            "number": self.number,
            "status": self.status,
            "seller_id": self.seller_id,
        }


class OrderHistoryModel(db.Model):
    __tablename__ = "order_history"

    number: Mapped[int] = mapped_column(ForeignKey(OrderModel.number), primary_key=True)
    status: Mapped[str] = mapped_column(primary_key=True)
    latitude: Mapped[str] = mapped_column()
    longitude: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column()

    def __init__(
        self,
        number: str,
        status: str,
        latitude: str,
        longitude: str,
        created_at: datetime,
    ) -> None:
        self.number = number
        self.status = status
        self.latitude = latitude
        self.longitude = longitude
        self.created_at = created_at

    def to_json(self):
        return {
            "number": self.number,
            "status": self.status,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "created_at": self.created_at.isoformat(),
        }


class Item(db.Model):
    __tablename__ = "item"

    sku: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    price: Mapped[float] = mapped_column(Float(2))
    seller_id: Mapped[UUID] = mapped_column(
        ForeignKey(SellerModel.id), primary_key=True
    )
    seller = relationship("SellerModel")

    def to_json(self):
        return {
            "sku": self.sku,
            "name": self.name,
            "description": self.description,
            "price": self.price,
        }
