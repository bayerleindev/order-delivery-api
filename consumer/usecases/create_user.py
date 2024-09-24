from sqlalchemy import or_
from auth.auth import Auth
from commons.base_exception import CustomBaseException
from commons.errors import ERROR_MESSAGES
from consumer.model import ConsumerModel
from consumer.repository import ConsumerRepository
from consumer.usecases.filter_consumer import FilterConsumer


class CreateUser:

    def __init__(self, repository: ConsumerRepository = None) -> None:
        self.repository = repository or ConsumerRepository()

    def execute(self, **kwargs):

        consumer = FilterConsumer(self.repository).execute(
            or_(
                ConsumerModel.email == kwargs["email"],
                ConsumerModel.document == kwargs["document"],
            )
        )

        if consumer:
            raise CustomBaseException(ERROR_MESSAGES["USER_EXISTS"]["pt"])

        consumer = ConsumerModel(
            document=kwargs["document"],
            name=kwargs["name"],
            last_name=kwargs["last_name"],
            email=kwargs["email"],
            phone=kwargs["phone"],
        )

        Auth().register(
            kwargs["email"],
            kwargs["password"],
            name=kwargs["name"],
            last_name=kwargs["last_name"],
            id=consumer.id,
        )

        self.repository.save(consumer)

        return consumer
