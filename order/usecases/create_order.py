import random
import string
from typing import Any, List
from uuid import UUID
from commons.base_exception import CustomBaseException
from commons.errors import get_error
from order.model import OrderModel
from order.repository import OrderRepository


class Input:
    seller_id: UUID
    consumer_id: UUID
    items: List[Any]
    address: Any

    def __init__(
        self, seller_id: UUID, consumer_id: UUID, items: List[Any], address: Any
    ) -> None:
        self.seller_id = seller_id
        self.consumer_id = consumer_id
        self.items = items
        self.address = address


class CreateOrder:
    def __init__(self, repository: OrderRepository = None) -> None:
        self.repository = repository or OrderRepository()

    def execute(self, input: Input):
        if not input.seller_id:
            raise CustomBaseException(get_error("INVALID_SELLER"))

        if not input.consumer_id:
            raise CustomBaseException(get_error("INVALID_CONSUMER"))

        if len(input.items) == 0:
            raise CustomBaseException(get_error("ORDER_WITHOUT_ITEM"))

        number = "".join(random.choices(string.digits, k=9))
        order = OrderModel(
            number=number,
            status="PENDING",
            seller_id=input.seller_id,
            consumer_id=input.consumer_id,
        )
        order.address = input.address
        order.items = input.items

        return self.repository.save(order)
