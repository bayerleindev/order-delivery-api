from auth.model import AuthModel, Role
from courier.model import CourierModel
from db_config import db_session


class CourierService:
    def save(self, **kwargs):
        with db_session.begin():
            courier = CourierModel(document=kwargs["document"], name=kwargs["name"])
            db_session.add(courier)

            user = AuthModel(
                email=kwargs["email"],
                password=kwargs["password"],
                identity_id=courier.id,
                roles=[Role.COURIER.value],
            )
            db_session.add(user)

        db_session.commit()
        db_session.refresh(courier)
        db_session.close()

        return courier

    def get_all(self):
        return [courier.to_json() for courier in db_session.query(CourierModel).all()]
