import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



def log_event(type, message):
    if type == "info":
        logger.info(message)
    elif type == "warning":
        logger.warning(message)
    elif type == "error":
        logger.error(message)
    else:
        logger.warning(f"Log type could not be found for: {message}")
    return