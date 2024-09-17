from courier.repository import CourierRepository
from order.repository import OrderRepository


class AssignOrderToCourier:

    def __init__(self) -> None:
        self.repository = CourierRepository()

    def execute(self, **kwargs):

        coordinates = kwargs["coordinates"]
        search_radius = 5000

        couriers = self.repository.find_nearest_courier(coordinates, search_radius)

        OrderRepository().assign_couriers(
            kwargs["order_number"],
            [
                courier.get("courier_id")
                for courier in couriers
                if courier.get("courier_id") is not None
            ],
        )
