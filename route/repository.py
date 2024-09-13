from db_config import db
from route.model import RouteModel, RouteOrderModel


class RouteRepository:

    def get_route(self, **kwargs):
        return (
            db.session.query(RouteModel)
            .filter_by(**kwargs)
            .order_by(RouteModel.created_at.desc())
            .first()
        )

    def get_orders(self, **kwargs):
        return db.session.query(RouteOrderModel).filter_by(**kwargs).all()
