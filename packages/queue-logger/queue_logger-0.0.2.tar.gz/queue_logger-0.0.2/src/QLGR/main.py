import logging
from .handler import RabbitMQHandler


def create_logger(name, log_level=logging.INFO):
    rabbitmq_handler = RabbitMQHandler()
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    logger.addHandler(rabbitmq_handler)
    return logger
