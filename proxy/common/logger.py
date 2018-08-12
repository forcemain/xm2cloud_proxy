#! -*- coding: utf-8 -*-

import logging


from proxy import settings


if settings.DEBUG:
    logging.basicConfig(level=settings.DEFAULT_LOG_LEVEL, format=settings.DEFAULT_LOG_FORMAT)


class Logger(object):
    @staticmethod
    def get_logger(name):
        logger = logging.getLogger(name)

        return logger
