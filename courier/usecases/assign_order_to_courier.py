from typing import List
from commons.scheduler import schedule
from commons.send_email import send_email
from courier.repository import CourierRepository
from order.repository import OrderRepository


class AssignOrderToCourier:

    def __init__(self) -> None:
        self.repository = CourierRepository()

    def execute(self, coordinates: List[float], order_number: str):

        search_radius = 5000

        couriers = self.repository.find_nearest_courier(coordinates, search_radius)

        if not couriers or len(couriers) == 0:
            schedule(
                self.execute,
                5,
                coordinates,
                order_number,
            )

        OrderRepository().assign_couriers(
            order_number,
            [
                courier.get("_id")
                for courier in couriers
                if courier.get("_id") is not None
            ],
        )

        send_email(
            "Aceitar pedido {} ? - courier {}".format(
                order_number, couriers[0].get("_id")
            ),
            "Novo pedido!",
        )
