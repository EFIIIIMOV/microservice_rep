#FROM python:3.10
#
## Выбор папки, в которой будет вестись работа
#WORKDIR /app_document
#
## Установка зависимостей проекта
#COPY ./requirements.txt /app_document/
#RUN pip install --no-cache-dir --upgrade -r /app_document/requirements.txt
#
## Перенос проекта в образ
#COPY ./app /app_document/app
#COPY .env /app_document
#
## Копирование файлов alembic
#COPY ./migration /app_document/migration
#COPY ./alembic.ini /app_document/alembic.ini
#
#EXPOSE 8080
#
## Добавляем путь к корневому каталогу проекта в PYTHONPATH
#ENV PYTHONPATH="${PYTHONPATH}:/app_document"
#ENV PYTHONPATH="${PYTHONPATH}:/app_document/app"
#
#CMD ["/bin/sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8080"]

FROM python:3.10

WORKDIR /microservice/app_document

# Установка зависимостей проекта
COPY ./requirements.txt /microservice/app_document/
RUN pip install --no-cache-dir --upgrade -r /microservice/app_document/requirements.txt

# Перенос проекта в образ
COPY ./app /microservice/app_document/app
COPY .env /microservice/app_document

# Копирование файлов alembic
COPY ./migration /microservice/app_document/migration
COPY ./alembic.ini /microservice/app_document/alembic.ini

EXPOSE  8080

# Добавляем путь к корневому каталогу проекта в PYTHONPATH
ENV PYTHONPATH="${PYTHONPATH}:/microservice/app_document"
ENV PYTHONPATH="${PYTHONPATH}:/microservice/app_document/app"

CMD ["/bin/sh", "-c", "alembic upgrade head && uvicorn app.main:app --host  0.0.0.0 --port  8080"]