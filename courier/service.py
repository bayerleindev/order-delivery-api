from auth.model import AuthModel, Role
from courier.model import CourierModel
from db_config import db


class CourierService:
    def save(self, **kwargs):
        with db.session.begin():
            courier = CourierModel(document=kwargs["document"], name=kwargs["name"])
            db.session.add(courier)

            user = AuthModel(
                email=kwargs["email"],
                password=kwargs["password"],
                identity_id=courier.id,
                roles=[Role.COURIER.value],
            )
            db.session.add(user)

        db.session.commit()
        db.session.refresh(courier)
        db.session.close()

        return courier

    def get_all(self):
        return [courier.to_json() for courier in db.session.query(CourierModel).all()]
