FROM python:3.10

# Выбор папки, в которой будет вестись работа
WORKDIR /app_document

# Установка зависимостей проекта
COPY ./app_document/requirements.txt /app_document/
RUN pip install --no-cache-dir --upgrade -r /app_document/requirements.txt

# Перенос проекта в образ
COPY ./app_document/app /app_document/app
COPY .env /app_document

# Копирование файлов alembic
COPY ./app_document/migration /app_document/migration
COPY ./app_document/alembic.ini /app_document/alembic.ini

EXPOSE 8080

CMD ["/bin/sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8080"]