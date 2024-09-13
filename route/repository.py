from uuid import UUID
from db_config import db_session
from order.model import OrderHistoryModel
from route.model import RouteModel, RouteOrderModel


class RouteRepository:

    def remove(self, **kwargs):
        db_session.query(RouteOrderModel).filter_by(
            route_id=kwargs["route_id"]
        ).filter_by(order_number=kwargs["order_number"]).delete()

        db_session.query(OrderHistoryModel).filter(
            OrderHistoryModel.number == kwargs["order_number"]
        ).delete()

    def save_or_update(self, route: RouteModel):
        db_session.add(route)
        return route

    def link_order_to_route(self, route_id: UUID, order_number: str):
        route_order = RouteOrderModel(order_number, route_id)
        db_session.add(route_order)
        return route_order

    def get_route(self, **kwargs):
        return (
            db_session.query(RouteModel)
            .filter_by(**kwargs)
            .order_by(RouteModel.created_at.desc())
            .first()
        )

    def get_orders(self, **kwargs):
        return db_session.query(RouteOrderModel).filter_by(**kwargs).all()
