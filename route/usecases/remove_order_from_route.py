from uuid import UUID
from order.usecases.load_order import LoadOrder
from order.usecases.update_order import Input, UpdateOrder
from route.exception import RouteException
from route.repository import RouteRepository
from route.route import Route
from route.usecases.get_route import GetRoute
from route.usecases.get_route_orders import GetRouteOrders


class RemoveOrderFromRoute:

    def __init__(self) -> None:
        self.repository = RouteRepository()

    def execute(self, **kwargs):
        route = GetRoute().execute(id=kwargs["route_id"])

        if route and route.status == "NEW":
            self.remove(kwargs["order_number"], route.id)
            orders = [
                order.order_number
                for order in GetRouteOrders().execute(route_id=route.id)
            ]
            return Route(
                route.id, route.status, [LoadOrder().execute(order) for order in orders]
            )
        raise RouteException(
            "Cannot remove order from route with status {}.".format(route.status)
        )

    def remove(self, order_number: str, route_id: UUID):

        self.repository.remove(order_number=order_number, route_id=route_id)

        UpdateOrder().execute(Input(order_number, status="PENDING"))
