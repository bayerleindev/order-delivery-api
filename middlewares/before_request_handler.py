from flask import Request
from commons.logger import Logger
from db_config import db_session

logger = Logger(__name__)


class BeforeRequestHandler:
    @staticmethod
    def handle(request: Request):
        print(request)
        logger.debug(message='Request incoming from address {addr}', addr=request.remote_addr)
        db_session.begin()
