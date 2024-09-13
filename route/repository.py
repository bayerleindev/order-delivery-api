from uuid import UUID
from db_config import db
from route.model import RouteModel, RouteOrderModel


class RouteRepository:

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
