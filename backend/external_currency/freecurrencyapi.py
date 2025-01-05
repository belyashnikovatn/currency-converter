"""Модуль для работы с freecurrencyapi сервисом."""

import os
from decimal import Decimal
from http import HTTPStatus

import requests
from django.core.cache import cache
from dotenv import load_dotenv
from external_currency import exceptions
from external_currency.config import logger

load_dotenv()

APIKEY = os.getenv('APIKEY')

HEADERS = {'apikey': APIKEY}

ENDPOINTS = {
    'latest': 'https://api.freecurrencyapi.com/v1/latest',
    'status': 'https://api.freecurrencyapi.com/v1/status',
}
"""Методы сервиса, нужные для работы:

latest - возвращает последний курс валют по USD
status - возвращает статус по бесплатной лицензии

"""


def get_api_answer(endpoint: str) -> dict:
    """Обращается по методу сервиса и выдаёт данные.

    Args:
        endpoint (str): метод сервиса

    Returns:
        dict: json-словарь

    """
    try:
        response = requests.get(
            ENDPOINTS[endpoint],
            headers=HEADERS,
        )
        if response.status_code != HTTPStatus.OK:
            error_message = f'Ошибка: статус ответа = {response.status_code}'
            logger.error(error_message)
            raise exceptions.NotOKStatusCodeException(error_message)
    except requests.RequestException as e:
        error_message = f'Ошибка: попытка запроса = {e}'
        logger.error(error_message)
        raise exceptions.NoResponse(error_message)

    try:
        return response.json()
    except requests.exceptions.JSONDecodeError as e:
        error_message = f'Ошибка: формат ответа = {e}'
        logger.error(error_message)
        raise exceptions.NoJSON(error_message)


def get_decimal(out: str, to: str,
                value: str) -> Decimal:
    """Производит расчет стоимости валюты.

    Args:
        out (str): значение валюты, из которой первести
        to (str): значение валюты, в которую первести
        value (str): количество для перевода

    Returns:
        decimal: результат расчёта
    """
    return Decimal(to) / Decimal(out) * Decimal(value)


def convert(out: str, to: str, value: str) -> Decimal:
    """Конвертирует по текущему курсу.

    Args:
        out (str): валюта, из которой первести
        to (str): валюта, в которую первести
        value (str): количество для перевода

    Returns:
        decimal: результат перевода
    """
    if cache.get(out) and cache.get(to):
        return get_decimal(cache.get(out), cache.get(to), value)

    rates = get_api_answer('latest')['data']
    if out not in rates:
        error_message = f'Нет валюты {out}'
        logger.error(error_message)
        raise exceptions.NoCurrency(error_message)
    if rates.get(out) == '0' or value == '0':
        error_message = 'Такой расчёт невозможен'
        logger.error(error_message)
        raise exceptions.DividedValueIsNull(error_message)
    if to not in rates:
        error_message = f'Нет валюты {to}'
        logger.error(error_message)
        raise exceptions.NoCurrency(error_message)
    return get_decimal(rates.get(out), rates.get(to), value)
