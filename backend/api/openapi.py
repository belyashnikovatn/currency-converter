from drf_spectacular.utils import (OpenApiParameter, extend_schema,
                                   extend_schema_view)
from rest_framework import status

from api.serializers import CurrencySerializer

currency = extend_schema_view(
    get=extend_schema(
        summary='Сконвертировать валюту',
        request=CurrencySerializer,
        responses={
            status.HTTP_200_OK: CurrencySerializer,
            status.HTTP_400_BAD_REQUEST: CurrencySerializer,
        },
        parameters=[
            OpenApiParameter(
                name='from',
                location=OpenApiParameter.QUERY,
                description='Валюта для конвертации',
                required=True,
                type=str),
            OpenApiParameter(
                name='to',
                location=OpenApiParameter.QUERY,
                description='Итоговая валюта ',
                required=True,
                type=str),
            OpenApiParameter(
                name='amount',
                location=OpenApiParameter.QUERY,
                description='Количество ',
                required=True,
                type=float),
        ],
    )
)
