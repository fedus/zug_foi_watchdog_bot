import logging

from datetime import datetime

from bot import publish_todays_message
from config import config

logging.basicConfig(encoding='utf-8')
logger = logging.getLogger(f"zug_foi_watchdog")
logger.setLevel(config.get("LOG_LEVEL", "INFO"))


def run() -> None:
    logger.info(f"ZUG FOI Watchdog bot started at {datetime.now()}")
    publish_todays_message()
    logger.info(f"Run finished at {datetime.now()}")


if __name__ == "__main__":
    run()
