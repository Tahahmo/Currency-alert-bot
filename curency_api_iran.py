import logging
import requests as requests

BASE_PATH = "https://exapi.sm4rt.ir/api/v1"

logger = logging.getLogger()


def get_i_all_currencies_list() -> list:
    logger.info("request to get all currencies")
    url = f"{BASE_PATH}/"
    headers = {"Authorization": "91ee072e-55b3-4389-96ab-78e160864ff1"}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        try:
            currency_list = data["data"]
            return currency_list
        except KeyError:
            logger.error("response for get all currencies has not data key")
            return list()
    else:
        logger.error("status code for this request is not 200")
        return list()


def i_convert_currency_price_to_irr(base: str) -> str:
    currency_list = get_i_all_currencies_list()
    if not currency_list:
        return ""
    for currency in currency_list:
        if (currency["ID"]).lower() == base.lower():
            return str(currency["price"])
    return ""
