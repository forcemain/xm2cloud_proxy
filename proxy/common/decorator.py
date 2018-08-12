#! -*- coding: utf-8 -*-


from proxy.common.logger import Logger


logger = Logger.get_logger(__name__)


def ignore_exception(error, exception_classes=(Exception,)):
    def _decorator(func):
        def _wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exception_classes:
                logger.error(error)
        return _wrapper
    return _decorator
