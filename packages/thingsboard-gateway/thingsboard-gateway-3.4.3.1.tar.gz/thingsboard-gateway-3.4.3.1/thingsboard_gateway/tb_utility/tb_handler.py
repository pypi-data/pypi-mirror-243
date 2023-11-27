#     Copyright 2023. ThingsBoard
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

import logging
import logging.handlers
from sys import stdout
from time import time
from os import environ

from thingsboard_gateway.tb_utility.tb_logger import TbLogger


class TBLoggerHandler(logging.Handler):
    LOGGER_NAME_TO_ATTRIBUTE_NAME = {
        'service': 'SERVICE_LOGS',
        'extension': 'EXTENSION_LOGS',
        'tb_connection': 'CONNECTION_LOGS',
        'storage': 'STORAGE_LOGS',
    }

    def __init__(self, gateway):
        self.current_log_level = 'INFO'
        super().__init__(logging.getLevelName(self.current_log_level))
        self.setLevel(logging.getLevelName('DEBUG'))
        self.__gateway = gateway
        self.activated = False
        self.setFormatter(logging.Formatter('%(asctime)s - |%(levelname)s| - [%(filename)s] - %(module)s - %(lineno)d - %(message)s'))
        self.loggers = ['service',
                        'extension',
                        'tb_connection',
                        'storage'
                        ]
        for logger in self.loggers:
            log = TbLogger(name=logger, gateway=gateway)
            log.addHandler(self.__gateway.main_handler)
            log.debug("Added remote handler to log %s", logger)

    def add_logger(self, name):
        log = TbLogger(name)
        log.addHandler(self.__gateway.main_handler)
        log.debug("Added remote handler to log %s", name)

    def activate(self, log_level=None):
        try:
            for logger in self.loggers:
                if log_level is not None and logging.getLevelName(log_level) is not None:
                    if logger == 'tb_connection' and log_level == 'DEBUG':
                        log = TbLogger(logger, gateway=self.__gateway)
                        log.setLevel(logging.getLevelName('INFO'))
                    else:
                        log = TbLogger(logger, gateway=self.__gateway)
                        self.current_log_level = log_level
                        log.setLevel(logging.getLevelName(log_level))
        except Exception as e:
            log = TbLogger('service')
            log.exception(e)
        self.activated = True

    def handle(self, record):
        if self.activated and not self.__gateway.stopped:
            name = record.name
            record = self.formatter.format(record)
            try:
                telemetry_key = self.LOGGER_NAME_TO_ATTRIBUTE_NAME[name]
            except KeyError:
                telemetry_key = name + '_LOGS'

            self.__gateway.tb_client.client.send_telemetry(
                {'ts': int(time() * 1000), 'values': {telemetry_key: record, 'LOGS': record}})

    def deactivate(self):
        self.activated = False

    @staticmethod
    def set_default_handler():
        logger_names = [
            'service',
            'storage',
            'extension',
            'tb_connection'
            ]
        for logger_name in logger_names:
            logger = TbLogger(logger_name)
            handler = logging.StreamHandler(stdout)
            handler.setFormatter(logging.Formatter('[STREAM ONLY] %(asctime)s - %(levelname)s - [%(filename)s] - %(module)s - %(lineno)d - %(message)s'))
            logger.addHandler(handler)


class TimedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
    def __init__(self, filename, when='h', interval=1, backupCount=0,
                 encoding=None, delay=False, utc=False):
        config_path = environ.get('logs')
        if config_path:
            filename = config_path + '/' + filename.split('/')[-1]

        super().__init__(filename, when=when, interval=interval, backupCount=backupCount,
                         encoding=encoding, delay=delay, utc=utc)
