import logging
from json import dumps


DISCARD_FILES_OTHER_LIB = ["kombu", "pika", "werkzeug"]
DISCARD_LEVELS_OTHER_LIB = [logging.INFO, logging.DEBUG]


def get_data_to_log(data) -> str:
    if isinstance(data, (dict, list)):
        return dumps(data)
    else:
        return str(data)


class LoggerFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> int:

        try:
            for each in DISCARD_FILES_OTHER_LIB:
                if (
                    each in record.pathname
                    and record.levelno in DISCARD_LEVELS_OTHER_LIB
                ):
                    return 0

        except Exception as err:
            record.filter_exception = f"[{str(err)}] - [{str(type(err))}]"
        return 1
