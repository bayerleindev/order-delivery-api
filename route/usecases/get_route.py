from db_config import db
from route.model import RouteModel


class GetRoute:
    def execute(self, **kwargs):
        return (
            db.session.query(RouteModel)
            .filter_by(**kwargs)
            .order_by(RouteModel.created_at.desc())
            .first()
        )
