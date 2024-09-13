from datetime import datetime
from order.exception import OrderException
from order.model import OrderHistoryModel
from order.repository import OrderRepository
from order.usecases.load_order import LoadOrder


class Input:
    order_number: str
    status: str
    latitude: str = "0.0"
    longitude: str = "0.0"

    def __init__(self, number: str, status: str) -> None:
        self.order_number = number
        self.status = status


class UpdateOrder:
    def __init__(self) -> None:
        self.repository = OrderRepository()

    def execute(self, input: Input):
        order = self.repository.filter(
            number=input.order_number
        ).first()  # db.session.query(OrderModel).filter_by(number=number).first()

        if not order:
            raise OrderException("Order '{}' not found".format(input.order_number))

        if order.status == input.status:
            return LoadOrder().execute(input.order_number)

        if self.__can_transit_to_status(order.status, input.status):
            order.status = input.status
            order.updated_at = datetime.now()

            self.repository.save_history(
                OrderHistoryModel(
                    number=input.order_number,
                    status=input.status,
                    latitude=input.latitude,
                    longitude=input.longitude,
                    created_at=datetime.now(),
                )
            )

            self.repository.update(order)

            return LoadOrder().execute(input.order_number)

        raise OrderException(
            "Order '{}' status cannot be updated from '{}' to '{}'".format(
                input.order_number, order.status, input.status
            )
        )

    def __can_transit_to_status(self, current_status: str, next_status: str) -> bool:
        allowed_transitions = {
            "PENDING": ["ACCEPTED"],
            "ACCEPTED": ["CONFIRMED", "REJECTED"],
            "CONFIRMED": ["IN_TRANSIT", "PENDING"],
            "IN_TRANSIT": ["ORDER_IN_TRANSIT"],
            "ORDER_IN_TRANSIT": ["ARRIVED"],
            "ARRIVED": ["DELIVERED", "CANCELLED"],
        }
        next_transitions = allowed_transitions.get(current_status, [])
        return next_status in next_transitions
