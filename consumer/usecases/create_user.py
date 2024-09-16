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
        self.repository.save(consumer)

        return consumer
