import logging
from typing import Literal


class APILogger:

    def __init__(self, enable_logs: bool = True):
        self.enable_logs = enable_logs
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger()

    def log_error(self, message):
        if self.enable_logs:
            self.logger.error(message)

    def log_info(self, message):
        if self.enable_logs:
            self.logger.info(message)

    def log_warning(self, message):
        if self.enable_logs:
            self.logger.warning(message)



    def log(self, message, level: Literal["warning", "info", "debug", "error"] = "info"):

        if self.enable_logs:
            if level == "info":
                self.logger.info(message)
            if level == "warning":
                self.logger.warning(message)
            if level == "error":
                self.logger.error(message)
