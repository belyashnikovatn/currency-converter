import time
from http import HTTPStatus

import pytest
from django.urls import reverse

from api.constants import AVAILABLE_CURRENCY


@pytest.mark.parametrize(
    'currency_from',
    AVAILABLE_CURRENCY,
)
@pytest.mark.parametrize(
    'currency_to',
    AVAILABLE_CURRENCY,
)
@pytest.mark.parametrize(
    'amount',
    (100, 100.0, 0)
)
def test_main_url_availability(client, currency_from, currency_to, amount):
    url = ''.join([
        reverse('api:convert'),
        f'?from={currency_from}&to={currency_to}&amount={amount}'
    ])
    time.sleep(5)  # to escape 429 ERROR
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
