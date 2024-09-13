from datetime import datetime
from uuid import UUID
from db_config import db
from order.model import OrderHistoryModel
from order.usecases.load_order import LoadOrder
from order.usecases.update_order import Input, UpdateOrder
from route.exception import RouteException
from route.model import RouteModel, RouteOrderModel
from route.route import Route
from route.usecases.get_route import GetRoute
from route.usecases.get_route_orders import GetRouteOrders


class RouteService:

    def link_order_to_route(self, route_id: UUID, order_number: str):
        route_order = RouteOrderModel(order_number, route_id)
        db.session.add(route_order)
        db.session.commit()
        return route_order

    def remove_order_from_route(self, route_id: UUID, order_number: str):
        db.session.query(RouteOrderModel).filter_by(route_id=route_id).filter_by(
            order_number=order_number
        ).delete()
        db.session.query(OrderHistoryModel).filter(
            OrderHistoryModel.number == order_number
        ).delete()
        db.session.commit()

        UpdateOrder().execute(Input(order_number, status="PENDING"))

    def save(self, **kwargs):
        courier_id = kwargs["courier_id"]
        id = kwargs["id"]
        route = RouteModel(courier_id, "NEW", datetime.now(), id)
        db.session.add(route)
        db.session.commit()
        return route

    def remove_order(self, route_id: UUID, order_number: str):
        route = GetRoute().execute(id=route_id)

        if route and route.status == "NEW":
            self.remove_order_from_route(route.id, order_number)
            orders = [
                order.order_number
                for order in GetRouteOrders().execute(route_id=route.id)
            ]
            return Route(
                route.id, route.status, [LoadOrder().execute(order) for order in orders]
            )
        raise RouteException(
            "Cannot remove order from route in status {}.".format(route.status)
        )
