import logging


def init_logger():
    """Настройка логирования."""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s, [%(levelname)s], %(message)s, %(funcName)s'
    )
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    logger.addHandler(handler)
    return logger


logger = init_logger()
