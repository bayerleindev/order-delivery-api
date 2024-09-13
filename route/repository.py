from uuid import UUID
from db_config import db
from order.model import OrderHistoryModel
from route.model import RouteModel, RouteOrderModel


class RouteRepository:

    def remove(self, **kwargs):
        db.session.query(RouteOrderModel).filter_by(
            route_id=kwargs["route_id"]
        ).filter_by(order_number=kwargs["order_number"]).delete()

        db.session.query(OrderHistoryModel).filter(
            OrderHistoryModel.number == kwargs["order_number"]
        ).delete()

        db.session.commit()

    def save_or_update(self, route: RouteModel):
        db.session.add(route)
        db.session.commit()
        return route

    def link_order_to_route(self, route_id: UUID, order_number: str):
        route_order = RouteOrderModel(order_number, route_id)
        db.session.add(route_order)
        db.session.commit()
        return route_order

    def get_route(self, **kwargs):
        return (
            db.session.query(RouteModel)
            .filter_by(**kwargs)
            .order_by(RouteModel.created_at.desc())
            .first()
        )

    def get_orders(self, **kwargs):
        return db.session.query(RouteOrderModel).filter_by(**kwargs).all()
