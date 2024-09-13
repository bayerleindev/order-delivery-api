from typing import Any


class Order:
    def __init__(
        self, number: str, status: str, items: Any = None, address: Any = None
    ) -> None:
        self.number = number
        self.status = status
        self.items = items
        self.address = address

    def to_json(self):
        return {
            "number": self.number,
            "status": self.status,
            "items": self.items,
            "address": self.address,
        }
