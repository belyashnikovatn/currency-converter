from decimal import Decimal

from external_currency.freecurrencyapi import convert
from rest_framework.response import Response
from rest_framework.views import APIView

from api import openapi
from api.serializers import CurrencySerializer


@openapi.currency
class CurrencyView(APIView):
    """
    Чтобы сконвертировать одну валюту в другую,
    используйте запрос с параметрами: from, to, amount.
    """

    def get(self, request, *args, **kwargs):
        serializer = CurrencySerializer(
            data=request.data,
            context={
                'request': request,
                'params': request.query_params,
                }
        )
        serializer.is_valid(raise_exception=True)

        from_param = request.query_params['from'].upper()
        to_param = request.query_params['to'].upper()
        amount_param = (request.query_params['amount']).replace(',', '.')

        result = convert(
            from_param, to_param, amount_param
        )
        return Response(
            {
                'info': {
                    'rate': result/Decimal(amount_param),
                },
                'query': request.query_params,
                'result': result
            }
        )
