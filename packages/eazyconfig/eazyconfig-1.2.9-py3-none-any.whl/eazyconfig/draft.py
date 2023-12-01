import logging
import colorlog

from constants import Format



def get_logger(name: str, filename: str=None, level=logging.INFO):
    logger = logging.getLogger(name)

    if filename is not None:
        logging.basicConfig(
            filename=filename,
            format=Format.file_log.value
        )

    handler = colorlog.StreamHandler()
    handler.setFormatter(
        colorlog.ColoredFormatter(
            Format.stream_log.value,
            datefmt="%Y-%m-%d %H:%M:%S %Z")
    )
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger


logger = get_logger(__name__, "bulshit.txt")

logger.info("Hi!")