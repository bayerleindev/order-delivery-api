from sqlalchemy import or_
from consumer.repository import ConsumerRepository


class FilterConsumer:

    def __init__(self, repository: ConsumerRepository = None) -> None:
        self.repository = repository or ConsumerRepository()

    def execute(self, filter: or_):
        consumer = self.repository.filter(filter).first()
        if consumer:
            return consumer.to_json()
        return None
