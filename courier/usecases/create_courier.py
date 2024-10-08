from auth.auth import Auth
from commons.base_exception import CustomBaseException
from commons.errors import ERROR_MESSAGES
from courier.model import CourierModel
from courier.repository import CourierRepository


class CreateCourier:

    def __init__(self) -> None:
        self.repository = CourierRepository()

    def execute(self, **kwargs):
        courier = CourierModel(document=kwargs["document"], name=kwargs["name"])

        identity = Auth().register(
            email=kwargs["email"],
            password=kwargs["password"],
            name=kwargs["name"],
            last_name=kwargs["last_name"],
            id=courier.id,
        )

        if identity.ok:
            self.repository.save(courier)
            return courier
        raise CustomBaseException(ERROR_MESSAGES["USER_EXISTS"]["pt"])
