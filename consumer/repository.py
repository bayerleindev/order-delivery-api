from consumer.model import ConsumerModel

from db_config import db_session


class ConsumerRepository:
    def save(self, consumer: ConsumerModel):
        db_session.add(consumer)
