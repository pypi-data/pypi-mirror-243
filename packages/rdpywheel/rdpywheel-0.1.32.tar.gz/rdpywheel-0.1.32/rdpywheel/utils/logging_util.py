import logging
from logging.handlers import RotatingFileHandler
import os


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class Logger:

    def __init__(self, name = "logs/normal.log", level=logging.DEBUG,file_name=None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.file_name = file_name
        self.add_console_handler()
        self.add_file_handler(name)

    def add_console_handler(self):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

    def add_file_handler(self, filename, max_bytes=10240000, backup_count=3, level=logging.DEBUG):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "a"):
            pass
        file_handler = RotatingFileHandler(filename, maxBytes=max_bytes, backupCount=backup_count)
        file_handler.setLevel(level)
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message: object, filename=None, *args: object):
        if filename:
            file_handler = self._get_file_handler(filename)
            file_handler.setLevel(logging.INFO)
            self.logger.addHandler(file_handler)
            self.logger.info(message,*args)
            self.logger.removeHandler(file_handler)
        else:
            self.logger.info(message)

    def warning(self, message, filename=None):
        if filename:
            file_handler = self._get_file_handler(filename)
            file_handler.setLevel(logging.WARNING)
            self.logger.addHandler(file_handler)
            self.logger.warning(message)
            self.logger.removeHandler(file_handler)
        else:
            self.logger.warning(message)

    def error(self, message, filename=None, *args: object):
        if filename:
            file_handler = self._get_file_handler(filename)
            file_handler.setLevel(logging.ERROR)
            self.logger.addHandler(file_handler)
            self.logger.error(message, args)
            self.logger.removeHandler(file_handler)
        else:
            self.logger.error(message)

    def critical(self, message, filename=None):
        if filename:
            file_handler = self._get_file_handler(filename)
            file_handler.setLevel(logging.CRITICAL)
            self.logger.addHandler(file_handler)
            self.logger.critical(message)
            self.logger.removeHandler(file_handler)
        else:
            self.logger.critical(message)

    def _get_file_handler(self, filename):
        for handler in self.logger.handlers:
            if isinstance(handler, logging.FileHandler) and handler.baseFilename == filename:
                return handler
            else:
                file_handler = logging.FileHandler(filename)
                file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                file_handler.setFormatter(file_formatter)
                return file_handler


    def slots_info(self, message):
        self.info(message, 'logs/slots_info.log')

    def schedule_success(self, message):
        self.info(message, 'logs/schedule_success.log')

    def schedule_failure(self, message):
        self.info(message, 'logs/schedule_failure.log')

    def login_info(self, message):
        self.info(message, 'logs/login_success.log')

    def login_error(self, message, *args: object):
        self.error(message, 'logs/normal.log', *args)

    def slots_response_cache(self, message):
        self.info(message, 'logs/slots_response_cache.log')

    def account_sessions(self, message):
        self.info(message, 'logs/account_sessions.log')
    def synchronous_data(self, message):
        self.info(message, 'logs/synchronous_data.log')

    def applicants_urn(self, message):
        self.info(message, 'logs/applicants_urn.log')
    def log_429(self, message):
        self.info(message, 'logs/429.log')

