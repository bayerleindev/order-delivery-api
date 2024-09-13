from db_config import db_session


class BeforeRequestHandler:
    @staticmethod
    def handle():
        db_session.begin()
