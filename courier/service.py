from auth.auth import Auth
from courier.model import CourierModel
from db_config import db_session


class CourierService:
    def save(self, **kwargs):

        courier = CourierModel(document=kwargs["document"], name=kwargs["name"])

        identity = Auth().register(
            kwargs["email"],
            kwargs["password"],
            name=kwargs["name"],
            last_name=kwargs["last_name"],
            id=courier.id,
        )

        if identity.ok:
            db_session.add(courier)
        return identity.json()

    def get_all(self):
        return [courier.to_json() for courier in db_session.query(CourierModel).all()]
