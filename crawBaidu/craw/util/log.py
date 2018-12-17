import logging
logging.getLogger().setLevel(logging.INFO)

def info(msg, *args, **kwargs):
    return logging.info(msg, *args, **kwargs)

def warn(msg, *args, **kwargs):
    return logging.warning(msg, *args, **kwargs)

def error(msg, *args, **kwargs):
    return logging.error(msg, *args, **kwargs)

def debug(msg, *args, **kwargs):
    return logging.debug(msg, *args, **kwargs)

def notset(msg, *args, **kwargs):
    return logging.debug(msg, *args, **kwargs)