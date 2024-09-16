from courier.model import CourierModel
from db_config import db_session


class CourierRepository:
    def save(self, courier: CourierModel):
        db_session.add(courier)
