import logging
import sys


def get_logger(name):
    """
    get standard logger to stdout, level INFO
    :param name:
    :return:
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(module)s | %(levelname)-" + str(len("CRITICAL")) + "s | %(message)s",
        datefmt='%Y/%m/%d %H:%M:%S',
        stream=sys.stdout
    )
    logger = logging.getLogger(name)
    return logger
