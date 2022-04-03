import logging

import arrow

from tweet_service import tweet_service

logger = logging.getLogger(f"zug_foi_watchdog.{__name__}")

LU_TZ = "Europe/Luxembourg"

DATE_OF_FOI = arrow.Arrow(2021, 12, 6, tzinfo=LU_TZ)
DATE_OF_CAD = arrow.Arrow(2022, 3, 2, tzinfo=LU_TZ)

def publish_todays_message():
    now_lux = arrow.now(LU_TZ)

    delta_foi = now_lux - DATE_OF_FOI
    delta_cad = now_lux - DATE_OF_CAD

    message = "🤔 Has @CityLuxembourg responded to @zug_lu 's FOI request yet?" + \
        "\n\n❌ NO.\n\n" + \
        f"🗓️ Days since FOI request: {delta_foi.days}\n" + \
        f"🗓️ Days since the CAD's confirmation: {delta_cad.days}" + \
        "\n\n@P_Goldschmidt"

    try:
        logger.debug("Attempting to tweet")
        logger.debug(message)
        tweet_service.tweet_thread(message)
    except Exception:
        logger.error(f"Error while tweeting!", exc_info=True)
