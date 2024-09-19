import json
import logging
import os


class Logger:
    logging.basicConfig(
        level=os.environ.get('LOG_LEVEL'),
        format="[{asctime}] [{levelname}] {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    log_data = {}

    def __init__(self, module) -> None:
        self.logger = logging.getLogger(module)
        self.module = module

    def info(self, message, **kwargs):
        self._log(self.logger.info, message, **kwargs)

    def error(self, message, **kwargs):
        self._log(self.logger.error, message, **kwargs)

    def debug(self, message, **kwargs):
        self._log(self.logger.debug, message, **kwargs)

    def warn(self, message, **kwargs):
        self._log(self.logger.warn, message, **kwargs)

    def _log(self, log_method, message: str, **kwargs):
        msg = message if not kwargs else message.format(**kwargs)
        self.log_data.update({"message": msg})
        self.log_data.update({"file": self.module})
        log_method(json.dumps(self.log_data))
