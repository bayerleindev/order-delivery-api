from auth.auth import Auth
from courier.model import CourierModel
from courier.repository import CourierRepository


class CreateCourier:

    def __init__(self) -> None:
        self.repository = CourierRepository()

    def execute(self, **kwargs):
        courier = CourierModel(document=kwargs["document"], name=kwargs["name"])

        identity = Auth().register(
            kwargs["email"],
            kwargs["password"],
            name=kwargs["name"],
            last_name=kwargs["last_name"],
            id=courier.id,
        )

        if identity.ok:
            self.repository.save(courier)
            return courier.to_json()
        return identity.json()
