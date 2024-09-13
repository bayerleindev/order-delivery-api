from datetime import datetime
from typing import List, Literal, get_args
from uuid import uuid4, UUID
from courier.model import CourierModel
from db_config import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Enum

from order.model import OrderModel

RouteStatus = Literal["NEW", "IN_TRAFFIC", "FINALIZED", "ABORTED"]


class RouteModel(db.Model):
    __tablename__ = "route"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    courier_id: Mapped[UUID] = mapped_column(ForeignKey(CourierModel.id), index=True)
    status: Mapped[RouteStatus] = mapped_column(
        Enum(
            *get_args(RouteStatus),
            name="status",
            create_constraint=True,
            validate_strings=True
        )
    )
    created_at: Mapped[datetime] = mapped_column()

    orders: List[str] = []

    def __init__(
        self,
        courier_id: UUID,
        status: RouteStatus,
        created_at: datetime,
        id: UUID = None,
    ) -> None:
        self.courier_id = courier_id
        self.status = status
        self.created_at = created_at
        if id:
            self.id = id

    def to_json(self):
        return {
            "id": str(self.id),
            "status": str(self.status),
            "created_at": str(self.created_at),
            "orders": self.orders,
        }


class RouteOrderModel(db.Model):
    __tablename__ = "route_order"
    order_number: Mapped[str] = mapped_column(
        ForeignKey(OrderModel.number), primary_key=True
    )
    route_id: Mapped[UUID] = mapped_column(ForeignKey(RouteModel.id), primary_key=True)

    def __init__(self, order_number: UUID, route_id: UUID) -> None:
        self.order_number = order_number
        self.route_id = route_id
