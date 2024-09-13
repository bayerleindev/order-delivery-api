from datetime import datetime
from uuid import UUID
from db_config import db
from order.model import OrderHistoryModel
from order.usecases.filter_order import FilterOrder
from order.usecases.load_order import LoadOrder
from order.usecases.update_order import Input, UpdateOrder
from route.exception import RouteException
from route.model import RouteModel, RouteOrderModel
from route.route import Route


class RouteService:
    def get_route(self, **kwargs):
        return (
            db.session.query(RouteModel)
            .filter_by(**kwargs)
            .order_by(RouteModel.created_at.desc())
            .first()
        )

    def load_orders(self, route_id: UUID):
        return db.session.query(RouteOrderModel).filter_by(route_id=route_id).all()

    def get_latest_route(self, courier: UUID):
        route = self.get_route(courier_id=courier)
        orders = [order.order_number for order in self.load_orders(route.id)]
        return Route(
            route.id, route.status, [LoadOrder().execute(order) for order in orders]
        )

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
        route = self.get_route(id=route_id)

        if route and route.status == "NEW":
            self.remove_order_from_route(route.id, order_number)
            orders = [order.order_number for order in self.load_orders(route.id)]
            return Route(
                route.id, route.status, [LoadOrder().execute(order) for order in orders]
            )
        raise RouteException(
            "Cannot remove order from route in status {}.".format(route.status)
        )

    def add_order_to_active_route(self, courier_id: UUID, order_number: str):
        route = self.get_route(courier_id=courier_id)

        if not route or route.status in ["FINALIZED", "ABORTED"]:
            route = self.save(courier_id=courier_id, id=id)

        if str(route.courier_id) != str(courier_id):
            raise RouteException("Route not found.")

        if route.status != "NEW":
            raise RouteException("Finish your opened route before creating a new one.")

        orders = [order.order_number for order in self.load_orders(route.id)]

        if order_number in orders:
            return Route(
                route.id, route.status, [LoadOrder().execute(order) for order in orders]
            )

        orders.append(order_number)

        UpdateOrder().execute(Input(order_number, status="CONFIRMED"))
        self.link_order_to_route(route.id, order_number)
        return Route(
            route.id, route.status, [LoadOrder().execute(order) for order in orders]
        )

    def start_route(self, route: RouteModel):
        if route.status == "IN_TRAFFIC":
            return Route(route.id, route.status, self.load_orders(route.id))

        if route.status != "NEW":
            raise RouteException(
                "Route in status {} cannot be started.".format(route.status)
            )

        route_orders = self.load_orders(route.id)

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
        db.session.commit()
        return Route(route.id, route.status, orders)

    def finish_route(self, route: RouteModel):
        if route.status != "IN_TRAFFIC":
            raise RouteException(
                "Route in status {} cannot be finished.".format(route.status)
            )

        route_orders = self.load_orders(route.id)

        for route_order in route_orders:
            order = FilterOrder().execute(number=route_order.order_number).first()
            if order and not order.is_finalized():
                raise RouteException(
                    "Route in status {} cannot be finished. Order {} is in still {}.".format(
                        route.status, order.number, order.status
                    )
                )

            route.status = "FINALIZED"
            db.session.commit()
            return Route(
                route.id,
                route.status,
                [LoadOrder().execute(order.order_number) for order in route_orders],
            )

    def update_status(self, **kwargs):
        status = kwargs["status"]
        courier = kwargs["courier"]

        route = self.get_route(courier_id=courier)
        # route = self.get_route(id=id)

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
                    for order in self.load_orders(route.id)
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
