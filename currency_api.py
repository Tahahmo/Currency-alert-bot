import requests as requests
import logging
from typing import Final

API_KEY: Final = ""
BASE_PATH = "https://openexchangerates.org/api/"
END_POINT = "latest.json"

logger = logging.getLogger()


def get_currency_list(base: str) -> dict:
    logger.info("request to get currency %s", base)
    url = f"{BASE_PATH}/{END_POINT}?app_id={API_KEY}&base={base}"
    resp = requests.get(url)
    if resp.status_code == 200 :
        data = resp.json()
        try:
            price_list = data["rates"]
            return price_list
        except KeyError:
            logger.error("Response for request get currency %s has no rates value", base)
            return dict()
    else:
        logger.error("response for request get currency %s is not 200! ")
        return dict()


def currency_price_convert_to_irr(base: str) -> str:
    price_list = get_currency_list(base)
    if not price_list:
        return ""
    try:
        return price_list["IRR"]
    except KeyError:
        logging.error("Error")
        return ""

