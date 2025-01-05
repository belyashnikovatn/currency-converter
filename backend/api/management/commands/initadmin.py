import os
from dotenv import load_dotenv

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from external_currency.config import logger


load_dotenv()
User = get_user_model()


class Command(BaseCommand):
    help = 'Создаёт админа по данным из env файла.'

    def handle(self, *args, **options):

        username = os.getenv('username', 'admin')
        email = os.getenv('email', 'belyashnikova.tn@gmail.com')
        password = os.getenv('password', '12345678')

        if not User.objects.filter(username=username).exists():
            try:
                User.objects.create_superuser(
                    email=email, username=username,
                    password=password
                )
                logger.info('Админ успешно создан.')
            except Exception as error:
                logger.error(f'Ошибка {error}!')
        else:
            logger.info('Админ уже создан.')
