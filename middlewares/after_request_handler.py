import json
from flask import Response
from db_config import db_session


class AfterRequestHandler:
    @staticmethod
    def handle(response: Response):
        if response and response.status_code < 500:
            response.set_data(json.dumps({"data": response.get_json()}))
            db_session.commit()
        else:
            response.set_data(json.dumps({"error": response.get_json()}))
            db_session.rollback()
        db_session.remove()

        return response
