import logging

from stalker.utils import directoryUtils

formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s', datefmt='%H:%M:%S')


def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

def createLogger():
    directoryUtils.createIfNotExists("./logs")

    # Logger
    app = setup_logger('logger', './logs/app.log')
    app.info("Started new session")
    return app
