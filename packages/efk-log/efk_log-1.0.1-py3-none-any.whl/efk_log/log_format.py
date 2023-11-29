import logging
import uuid

from efk_log.logger_json import JsonFormatter, TRACE_ID_CONTEXT

try:
    from concurrent_log_handler import ConcurrentRotatingFileHandler as RotatingFileHandler
except Exception as e:
    from logging.handlers import RotatingFileHandler


def set_trace_code(trace_code=None):
    if trace_code is None:
        trace_code = uuid.uuid4()
    TRACE_ID_CONTEXT.set(str(trace_code))


class LogJsonFormat:
    SUPPORTED_KEYS = [
        'asctime',
        'host',
        'project',
        'logtype',
        'levelname',
        'trace_code',
        'funcName',
        # 'module',
        'filename',
        'lineno',
        'message',
        # 'msecs',
        # 'asctime_s',
        # 'process',
        # 'thread',
        # 'created',
        # 'threadName',
        # 'name',
        # 'relativeCreated',
        # 'processName',
        # 'pathname',
    ]

    def __init__(self, file_path, console=False, project=None):

        # log_handler = logging.FileHandler(filename=file_path, mode='a', encoding='U8')
        set_trace_code()
        formatter = JsonFormatter(
            ' '.join(['%({0:s})'.format(i) for i in self.SUPPORTED_KEYS]),
            json_ensure_ascii=False,
            project=project
        )
        logger = logging.getLogger()
        logger.handlers = []
        logger.setLevel(logging.INFO)

        if file_path:
            import os
            file_path = '{}/{}.log'.format(file_path, project)
            if os.path.exists(os.path.dirname(file_path)):
                pass
            else:
                os.makedirs(os.path.dirname(file_path))
            log_handler = RotatingFileHandler(filename=file_path, backupCount=10, mode='a', encoding='U8',
                                              maxBytes=1024 * 1024 * 520)
            log_handler.setFormatter(formatter)
            logger.addHandler(log_handler)
        if console:
            handler_console = logging.StreamHandler()
            handler_console.setLevel(logging.INFO)
            handler_console.setFormatter(formatter)
            logger.addHandler(handler_console)
