from flask import Response
from db_config import db_session


class AfterRequestHandler:
    @staticmethod
    def handle(response: Response):
        if response and response.status_code < 500:
            db_session.commit()
        else:
            db_session.rollback()
        db_session.remove()
