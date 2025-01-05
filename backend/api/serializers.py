from typing import Union

from rest_framework import serializers

from currency_converter.constants import AVAILABLE_CURRENCY


class CurrencySerializer(serializers.Serializer):
    """
    Проверяет наличие всех параметров
    Проверяет валюты из списка доступных (список в constants)
    Проверяет тип для количества
    """

    def check_currency(self, currency: str) -> Union[str, None]:
        if currency.upper() not in AVAILABLE_CURRENCY:
            return (f'{currency}! Введите валюту'
                    f' из списка: {AVAILABLE_CURRENCY}')
        return None

    def validate(self, data: dict) -> dict:
        out = self.context['params'].get('from')
        to = self.context['params'].get('to')
        amount = (self.context['params'].get('amount')).replace(',', '.')
        # проверяем наличие параметра: валюта из
        if not out:
            raise serializers.ValidationError('Введите параметр from')
        # проверяем значение: валюта
        if message := self.check_currency(out):
            raise serializers.ValidationError(message)
        # проверяем наличие параметра: валюта в
        if not to:
            raise serializers.ValidationError('Введите параметр to')
        # проверяем значение: валюта
        if message := self.check_currency(to):
            raise serializers.ValidationError(message)
        # проверяем наличие параметра: кол-во
        if not amount:
            raise serializers.ValidationError('Введите параметр amount')
        # проверяем тип и значение = число > 0
        try:
            float(amount)
        except ValueError:
            raise serializers.ValidationError(
                'Количество должно быть числом')
        if float(amount) <= 0:
            raise serializers.ValidationError(
                'Количество должно быть больше 0')
        return data
