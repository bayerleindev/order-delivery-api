from datetime import datetime
from order.usecases.load_order import LoadOrder
from order.usecases.update_order import Input, UpdateOrder
from route.exception import RouteException
from route.model import RouteModel
from route.repository import RouteRepository
from route.route import Route
from route.usecases.get_route import GetRoute
from route.usecases.get_route_orders import GetRouteOrders


class AddOrderToRoute:

    def __init__(self) -> None:
        self.repository = RouteRepository()

    def execute(self, **kwargs):
        order_number = kwargs["order_number"]
        route = GetRoute().execute(courier_id=kwargs["courier"])

        if not route or route.status in ["FINALIZED", "ABORTED"]:
            route = self.repository.save_or_update(
                RouteModel(kwargs["courier"], "NEW", datetime.now())
            )

        if str(route.courier_id) != str(kwargs["courier"]):
            raise RouteException("Route not found.")

        if route.status != "NEW":
            raise RouteException("Finish your opened route before creating a new one.")

        orders = [
            order.order_number for order in GetRouteOrders().execute(route_id=route.id)
        ]

        if order_number in orders:
            return Route(
                route.id, route.status, [LoadOrder().execute(order) for order in orders]
            )

        orders.append(order_number)

        UpdateOrder().execute(Input(order_number, status="CONFIRMED"))
        self.repository.link_order_to_route(route.id, order_number)
        return Route(
            route.id, route.status, [LoadOrder().execute(order) for order in orders]
        )
