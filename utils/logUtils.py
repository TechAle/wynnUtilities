import logging

from utils import fileUtils

formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s', datefmt='%H:%M:%S')
HUNTED_LEVEL_NUM = 36
logging.addLevelName(HUNTED_LEVEL_NUM, "HUNTED")


def hunted(self, message, *args, **kws):
    if self.isEnabledFor(HUNTED_LEVEL_NUM):
        # Yes, logger takes its '*args' as 'args'.
        self._log(HUNTED_LEVEL_NUM, message, args, **kws)

logging.hunted = hunted
logging.Logger.hunted = hunted

HUNTER_LEVEL_NUM = 35
logging.addLevelName(HUNTER_LEVEL_NUM, "HUNTER")


def hunter(self, message, *args, **kws):
    if self.isEnabledFor(HUNTED_LEVEL_NUM):
        # Yes, logger takes its '*args' as 'args'.
        self._log(HUNTER_LEVEL_NUM, message, args, **kws)


logging.Logger.hunter = hunter
logging.hunter = hunter

def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


def createLogger(name):
    if len(name.split("/")) > 1:
        fileUtils.createDirectoryIfNotExists("./" + name.split("/")[1] + "/logs")
        app = setup_logger(name, name + '.log')
    else:
        fileUtils.createDirectoryIfNotExists("./logs")
        app = setup_logger(name, './logs/' + name + '.log')

    app.info("Started new session")
    return app
