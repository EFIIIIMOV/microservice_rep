import aio_pika
import json
import traceback
from asyncio import AbstractEventLoop
from aio_pika.abc import AbstractRobustConnection
from aio_pika import connect_robust, IncomingMessage
from uuid import UUID

from app.settings import settings
from app.services.document_service import DocumentService
from app.repositories.local_document_repo import DocumentRepo

#
# async def send_to_document_queue(data: dict):
#     try:
#         # Установка соединения с RabbitMQ
#         connection = await aio_pika.connect_robust(settings.amqp_url)
#
#         async with connection:
#             # Создание канала
#             channel = await connection.channel()
#
#             # Объявление очереди, если её нет
#             queue = await channel.declare_queue('document_created_queue', durable=True)
#
#             # Отправка данных в очередь
#             await channel.default_exchange.publish(
#                 aio_pika.Message(body=json.dumps(data).encode()),
#                 routing_key='document_created_queue'
#             )
#             print(" [x] Sent %r" % data)
#
#     except aio_pika.exceptions.AMQPError as e:
#         print(f"Error occurred while sending data to queue: {e}")
#
#     finally:
#         # Закрытие соединения после отправки данных в очередь
#         await connection.close()

async def send_to_document_queue(data: dict):
    try:
        # Установка соединения с RabbitMQ
        connection = await aio_pika.connect_robust(settings.amqp_url)

        async with connection:
            # Создание канала
            channel = await connection.channel()

            # Объявление очереди, если её нет
            queue = await channel.declare_queue('document_created_queue', durable=True)

            # Преобразование UUID в строку перед сериализацией в JSON
            for key, value in data.items():
                if isinstance(value, UUID):
                    data[key] = str(value)

            # Отправка данных в очередь
            await channel.default_exchange.publish(
                aio_pika.Message(body=json.dumps(data).encode()),
                routing_key='document_created_queue'
            )
            print(" [x] Sent %r" % data)

    except aio_pika.exceptions.AMQPError as e:
        print(f"Error occurred while sending data to queue: {e}")

    finally:
        # Закрытие соединения после отправки данных в очередь
        await connection.close()

async def process_created_document(msg: IncomingMessage):
    try:
        data = json.loads(msg.body.decode())
        DocumentService(DocumentRepo()).create_document(
            data['doc_id'], data['ord_id'], data['type'], data['create_date'], data['completion_date'], data['doc'])
        await msg.ack()
    except:
        traceback.print_exc()
        await msg.ack()


async def consume(loop: AbstractEventLoop) -> AbstractRobustConnection:
    # connection = await connect_robust(settings.amqp_url, loop=loop)
    # channel = await connection.channel()

    connection = await aio_pika.connect_robust(settings.amqp_url, loop=loop)
    channel = await connection.channel()

    document_created_queue = await channel.declare_queue('document_created_queue', durable=True)
    # order_paid_queue = await channel.declare_queue('laptev_order_paid_queue', durable=True)

    # print('\n////document_created_queue = await channel.declare_queue////\n')

    await document_created_queue.consume(process_created_document)
    # await order_paid_queue.consume(process_paid_order)

    print('Started RabbitMQ consuming...')

    return connection
