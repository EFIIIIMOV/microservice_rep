FROM python:3.10

# Выбор папки, в которой будет вестись работа
WORKDIR /microservice

# Установка зависимостей проекта
COPY ./app_order/requirements.txt /app_order/
RUN pip install --no-cache-dir --upgrade -r /app_order/requirements.txt

# Перенос проекта в образ
COPY ./app_order/app /app_order/app
COPY ./app_order/env /app_order

# Копирование файлов alembic
COPY ./app_order/migration /app_order/migration
COPY ./app_order/alembic.ini /app_order/alembic.ini

EXPOSE 80

CMD ["/bin/sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 80"]

