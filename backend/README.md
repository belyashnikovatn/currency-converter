# Backend проекта "Сервис для конвертации валют"

Создание API и веб-приложения для конвертации валют с использованием актуальных данных о курсах валют от стороннего API.

Даты проведения: 3 декабря - 28 декабря 2024 года.

Организатор: АНО ДПО «Образовательные технологии Яндекса» (Яндекс.Практикум)

[Подробная информация о Хакатоне](https://docs.google.com/document/d/1nQz2IvNutPv28m0HGASbrWm13tV1RCPeAaySq19uk1w/edit?tab=t.0)

### Опубликованное приложение

[Ссылка на сайт](https://currency-converter-team2.vercel.app/)

[Фронтенд приложения](https://github.com/hackathon-team-2/currency-converter-frontend)

[Бэкенд приложения](https://github.com/hackathon-team-2/currency-converter-backend)

[Макет в Figma](https://www.figma.com/design/PHxF5BGFK2kv0NvCDQu1xE/%D0%9A%D0%BE%D0%BD%D0%B2%D0%B5%D1%80%D1%82%D0%B5%D1%80?node-id=1-3&t=hhRhzISQrox11Nxz-0)

## Содержание
- [Технологии](#технологии)
- [Локальный запуск проекта](#локальный-запуск-проекта)
- [Структура проекта](#структура-проекта)
- [Развёртывание на сервере](#развертывание-проекта-на-удаленном-сервере)


## Технологии:
### Frontend
HTML5, JavaScript ES6, Sass / SCSS
### Backend
Python, Django REST Framework, drf-spectacular, Redis, Celery, Nginx, Docker, GitHub Actions, Gunicorn, corsheaders


## Локальный запуск проекта
1. Склонируйте проекта с git-репозитория и перейдите в корневую директорию проекта:
```bash
git clone https://github.com/hackathon-team-2/currency-converter-backend.git
cd currency-converter-backend
```
2. Используйте .env.example и создайте свой .env:
```
APIKEY                        - токен можно получить здесь - https://freecurrencyapi.com/                
DB_HOST='postgres_db'         - должен совпадать с названием сервиса postgres_db в docker-compose
```

3. В терминал для запуска выполните команду:

```bash
docker compose up --build  
```

4. В отдельном терминале из корневой директории проекта выполните команды:
```bash
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py collectstatic
docker compose exec backend sh -c 'cp -r /app/collected_static/. /backend_static/static/'
```

5. Для создания админа выполните команду:
```bash
docker compose exec backend python manage.py createsuperuser
```

6. Проект станет доступен [по ссылке](http://127.0.0.1:8000/api/convert/?from=USD&to=EUR&amount=1000)
<img src="screens/drf_interface.png" alt="drf_interface" style="float: left; margin-right: 10px;" />

7. Подробное описание станет доступно [по ссылке](http://127.0.0.1:8000/schema/swagger-ui/)
<img src="screens/swagger_interface.png" alt="swagger_interface" style="float: left; margin-right: 10px;" />

8. Админка станет доступна по адресу http://127.0.0.1:8000/admin/


## Структура проекта

### Приложение api - сервис для конвертации валюты
- Вью для get-запроса и обработки параметров  
- Сериализатор для проверки параметров: наличие, соответствие    

Запрос:  
```
http://127.0.0.1:8000/api/convert?from=USD&to=RUB&amount=125
```
  
Ответ:  
```json
{
  "info": {
    "rate": 100.0191775342
  },
  "query": {
    "amount": "125",
    "from": "USD",
    "to": "RUB"
  },
  "result": 12502.397191775
} 
```
Примеры запросов для тестирования сервиса:  
http://127.0.0.1:8000/api/convert?from=USD&to=EUR&amount=100  
http://127.0.0.1:8000/api/convert?from=rub&to=USD&amount=100  
http://127.0.0.1:8000/api/convert?from=RUB&to=eur&amount=5.5   
http://127.0.0.1:8000/api/convert?from=rub&to=qqq&amount=100   


### Freecurrencyapi - сторонний api-сервис, предоставляющий информацию о стоимости валют
Реализация интеграции с сервисом находится в файле api/external_currency/freecurrencyapi.py  
Чтобы отдельно протестировать работу сервиса:
1. Допишите в конце файла:  
```python
if __name__ == '__main__':
    result = convert('RUB', 'EUR', 10000)
    print(result)
```
2. Запустите файл:
```bash
python api/external_currency/freecurrencyapi.py
```

Документация на сервис - https://freecurrencyapi.com/docs/  
Для подключения к freecurrencyapi нужен apikey, бесплатный тариф имеет ограничения:   
"5k Free Monthly Requests + 32 World Currencies + All exchange rates are updated on a daily basis".  

### Конфиг для логирования
/api/external_currency/config.py

### Связь фронта с бэком:
Для связи фронта с бэкендом на удалённом сервере настроен nginx для обеспечения cors-политики.

## Развертывание проекта на удаленном сервере:
### Выполненные задачи для настройки сервера:
**Установить на сервере Docker, Docker Compose, Nginx и certbot:**
```
sudo apt update
sudo apt install curl                                   - установка утилиты для скачивания файлов
curl -fsSL https://get.docker.com -o get-docker.sh      - скачать скрипт для установки
sh get-docker.sh                                        - запуск скрипта
sudo apt-get install docker-compose-plugin              - последняя версия docker compose
sudo apt install nginx                                  - установка nginx
sudo systemctl start nginx                              - запуск nginx
sudo apt install snapd                                  - установка пакетного менеджера snap.
sudo snap install core; sudo snap refresh core          - установка и обновление зависимостей для пакетного менеджера snap
sudo snap install --classic certbot                     - установка certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot           - создание ссылки на certbot в системной директории для админа

```
**Создать на сервере директорию converter:**
```
mkdir converter
```

**Для работы с GitHub Actions необходимо в репозитории в разделе Secrets > Actions создать переменные окружения:**
```
DOCKER_PASSWORD         - пароль от Docker Hub
DOCKER_USERNAME         - логин Docker Hub
HOST                    - публичный IP сервера
USER                    - логин пользователя на сервере
SSH_KEY                 - приватный ssh-ключ
SSH_PASSPHRASE          - пароль для ssh-ключа
TELEGRAM_TO             - ID телеграм-аккаунта для посылки сообщения
TELEGRAM_TOKEN          - токен бота, посылающего сообщение
```
**На сервере в директории converter создать файл .env и внести туда ваши данные по примеру из .env.example:**             
Учтите, что
```
DB_HOST='postgres_db'         - должен совпадать с названием сервиса postgres_db в docker-compose
```
 
**На сервере настроить nginx:**
1. На сервере в редакторе nano откройте конфиг Nginx:
```
sudo nano /etc/nginx/sites-enabled/default
```
2. Замените весь код в файле на этот:
```
server {
    index index.html;
    server_tokens off;
    server_name currency-converter.hopto.org;


    location / {
        add_header 'Access-Control-Allow-Origin' '*';
        add_header 'Access-Control-Allow-Methods' 'GET';
        proxy_set_header Host $http_host;
        proxy_pass http://127.0.0.1:8000;
    }

}
```
Вместо currency-converter.hopto.org подставьте свой рабочий домен


3. Убедитесь, что в конфиге нет ошибок и перезапустите nginx:
```
sudo nginx -t
sudo service nginx reload
sudo systemctl restart nginx
```
4. Получите ssl сертификат:
```
sudo certbot --nginx
sudo nginx -t
sudo service nginx reload
```
**Склонируйте репозиторий на локальный компьютер:**
```
git clone https://github.com/hackathon-team-2/currency-converter-backend.git
```
### После каждого обновления репозитория (push в ветку main) будет происходить:

1. Проверка кода на соответствие стандарту PEP8 (с помощью пакета flake8)
2. Сборка и доставка докер-образов backend и gateway на Docker Hub
3. Разворачивание проекта на удаленном сервере
4. Отправка сообщения в Telegram в случае успеха

### Чтобы создать суперпользователя, после запуска проекта на сервере в директории /converter выполните команду:
```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py createsuperuser
```

## Проект доступен по адресам:
https://currency-converter.hopto.org/schema/swagger-ui/       - Swagger документация                          
https://currency-converter-livid-alpha.vercel.app/            - Готовый проект, связанный с фронтом                        
https://currency-converter.hopto.org/admin/                   - Админка, в которой можно управлять периодическими задачами                             
