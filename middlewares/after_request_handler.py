import json
from flask import Response
from psycopg2 import errors
from commons.base_exception import CustomBaseException
from commons.errors import ERROR_MESSAGES
from db_config import db_session
from sqlalchemy.exc import IntegrityError


class AfterRequestHandler:
    @staticmethod
    def handle(response: Response):
        try:
            if response and response.status_code < 500:
                response.set_data(json.dumps({"data": response.get_json()}))
                db_session.commit()
            else:
                response.set_data(json.dumps({"error": response.get_json()}))
                db_session.rollback()
            db_session.remove()
        except IntegrityError as e:
            if isinstance(e.orig, errors.UniqueViolation):
                raise CustomBaseException(ERROR_MESSAGES["USER_EXISTS"]["pt"])
        finally:
            return response
