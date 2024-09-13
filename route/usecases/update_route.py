from order.usecases.filter_order import FilterOrder
from order.usecases.load_order import LoadOrder
from order.usecases.update_order import Input, UpdateOrder
from route.exception import RouteException
from route.model import RouteModel
from route.repository import RouteRepository
from route.route import Route
from route.usecases.get_route import GetRoute
from route.usecases.get_route_orders import GetRouteOrders


class UpdateRoute:

    def __init__(self) -> None:
        self.repository = RouteRepository()

    def execute(self, **kwargs):
        status = kwargs["status"]
        courier = kwargs["courier"]

        route = GetRoute().execute(courier_id=courier)

        if not route:
            raise RouteException("Route not found.")

        if str(route.courier_id) != courier:
            raise RouteException("Route not found.")

        if route.status == status:
            return Route(
                route.id,
                route.status,
                [
                    LoadOrder().execute(order.order_number)
                    for order in GetRouteOrders().execute(route_id=route.id)
                ],
            )

        if self.__can_transit_to_status(route.status, status):
            if status == "IN_TRAFFIC":
                return self.start_route(route)
            if status == "FINALIZED":
                return self.finish_route(route)
        else:
            raise RouteException(
                "Route in status {} cannot be changed to {}.".format(
                    route.status, status
                )
            )

    def __can_transit_to_status(self, current_status: str, next_status: str):
        allowed_transitions = {
            "NEW": ["IN_TRAFFIC", "ABORTED"],
            "IN_TRAFFIC": ["FINALIZED", "ABORTED"],
        }
        next_transitions = allowed_transitions.get(current_status, [])
        return next_status in next_transitions

    def start_route(self, route: RouteModel):
        if route.status == "IN_TRAFFIC":
            return Route(
                route.id, route.status, GetRouteOrders().execute(route_id=route.id)
            )

        if route.status != "NEW":
            raise RouteException(
                "Route in status {} cannot be started.".format(route.status)
            )

        route_orders = GetRouteOrders().execute(route_id=route.id)

        if len(route_orders) == 0:
            raise RouteException("Add order to start route.")

        orders = []
        for route_order in route_orders:
            orders.append(
                UpdateOrder().execute(
                    Input(route_order.order_number, status="IN_TRANSIT")
                )
            )

        route.status = "IN_TRAFFIC"
        # db.session.commit()
        self.repository.save_or_update(route)
        return Route(route.id, route.status, orders)

    def finish_route(self, route: RouteModel):
        if route.status != "IN_TRAFFIC":
            raise RouteException(
                "Route in status {} cannot be finished.".format(route.status)
            )

        route_orders = GetRouteOrders().execute(route_id=route.id)

        for route_order in route_orders:
            order = FilterOrder().execute(number=route_order.order_number).first()
            if order and not order.is_finalized():
                raise RouteException(
                    "Route in status {} cannot be finished. Order {} is in still {}.".format(
                        route.status, order.number, order.status
                    )
                )

            route.status = "FINALIZED"
            # db.session.commit()
            self.repository.save_or_update(route)
            return Route(
                route.id,
                route.status,
                [LoadOrder().execute(order.order_number) for order in route_orders],
            )
