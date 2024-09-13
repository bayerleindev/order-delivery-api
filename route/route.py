from typing import Any
from uuid import UUID


class Route:
    def __init__(self, id: UUID, status: str, orders: Any) -> None:
        self.id = str(id)
        self.status = status
        self.orders = orders

    def to_json(self):
        return {
            "id": str(self.id),
            "status": self.status,
            "orders": self.orders,
        }
