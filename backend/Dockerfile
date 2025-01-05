FROM python:3.9

WORKDIR /app

COPY requirements/requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

ENTRYPOINT ["sh", "entrypoint.sh"]