from datetime import datetime
import json
import logging


class Logger:
    logging.basicConfig(
        level=logging.INFO,
        format="[{asctime}] [{levelname}] {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    
    log_data = { }

    def __init__(self, module) -> None:
        self.logger = logging.getLogger(module)
        self.module = module

    def info(self, message, *args):
        self._log(self.logger.info, message, *args)

    def error(self, message, *args):
        self._log(self.logger.error, message, *args)

    def debug(self, message, *args):
        self._log(self.logger.debug, message, *args)

    def warn(self, message, *args):
        self._log(self.logger.warn, message, *args)
    
    def _log(self, log_method, message: str, *args):
        msg = message if not args else message % args
        self.log_data.update({'message': msg})
        self.log_data.update({'file': self.module})
        log_method(json.dumps(self.log_data))
