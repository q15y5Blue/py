import logging
logging.getLogger().setLevel(logging.INFO)


def info(message):
    return logging.info(message)

def warn(message):
    return logging.warning(message)

def error(message):
    return logging.error(message)