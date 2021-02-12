import logging


def error_handler(obj, message):
    if not obj:
        logging.error(message)
        return []
