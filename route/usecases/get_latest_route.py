from order.usecases.load_order import LoadOrder
from route.route import Route
from route.usecases.get_route import GetRoute
from route.usecases.get_route_orders import GetRouteOrders


class GetLatestRoute:
    def execute(self, **kwargs):
        route = GetRoute().execute(courier_id=kwargs["courier"])
        orders = [
            order.order_number for order in GetRouteOrders().execute(route_id=route.id)
        ]
        return Route(
            route.id, route.status, [LoadOrder().execute(order) for order in orders]
        )
