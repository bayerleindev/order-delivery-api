from consumer.model import ConsumerModel
from db_config import db_session
from sqlalchemy import or_


class ConsumerRepository:
    def save(self, consumer: ConsumerModel):
        db_session.add(consumer)

    def filter(self, filter: or_):
        return db_session.query(ConsumerModel).filter(filter)
