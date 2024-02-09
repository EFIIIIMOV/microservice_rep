FROM python:3.10

# Выбор папки, в которой будет вестись работа
WORKDIR /code

# Установка зависимостей проекта
COPY ./requirements.txt /code/
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Перенос проекта в образ
COPY ./app /code/app
COPY .env /code

# Копирование файлов alembic
COPY ./migration /code/migration
COPY ./alembic.ini /code/alembic.ini

EXPOSE 8080

# Добавляем путь к корневому каталогу проекта в PYTHONPATH
ENV PYTHONPATH="${PYTHONPATH}:/microservice/app_document"
ENV PYTHONPATH="${PYTHONPATH}:/microservice/app_document/app"

CMD ["/bin/sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8080"]