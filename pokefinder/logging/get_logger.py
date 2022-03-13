"""mehtod to get a logger with attached formatting """
import logging
from pokefinder.logging.json_logger import FormatterJSON

def get_logger(log_level:str):
    """Method to get an logger with json formatted log messages.
    Parameters
    ----------
    log_level:str
        log -level to use in the logger.

    Returns
    -------
    logger: logging.Logger
        logger with attached formating

    """
    log_levels = {'INFO':logging.INFO,
    'WARNING':logging.WARNING,
    'DEBUG':logging.DEBUG}
    if log_level not in log_levels.keys():
        log_level=log_level.upper()

    logging.basicConfig(level=log_levels.get(log_level))
    logger = logging.getLogger()
    logger.setLevel('INFO')

    formatter = FormatterJSON(
        '[%(levelname)s]\t%(asctime)s.%(msecs)dZ\t%(levelno)s\t%(message)s\n',
        '%Y-%m-%dT%H:%M:%S'
    )
    logger.handlers[0].setFormatter(formatter)
    return logger
    