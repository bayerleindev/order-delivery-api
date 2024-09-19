from auth.auth import Auth
from commons.base_exception import CustomBaseException
from commons.errors import ERROR_MESSAGES
from consumer.model import ConsumerModel
from consumer.repository import ConsumerRepository


class CreateUser:

    def __init__(self, repository: ConsumerRepository = None) -> None:
        self.repository = repository or ConsumerRepository()

    def execute(self, **kwargs):
        consumer = ConsumerModel(
            document=kwargs["document"],
            name=kwargs["name"],
            email=kwargs["email"],
            phone=kwargs["phone"],
        )

        identity = Auth().register(
            kwargs["email"],
            kwargs["password"],
            name=kwargs["name"],
            last_name=kwargs["last_name"],
            id=consumer.id,
        )

        if identity.ok:
            self.repository.save(consumer)
            return consumer
        raise CustomBaseException(ERROR_MESSAGES["USER_EXISTS"]["pt"])
