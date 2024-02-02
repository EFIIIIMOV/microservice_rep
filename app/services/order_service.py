# 1. Поменять int на UUID в функциях

from uuid import UUID
from fastapi import Depends
from datetime import datetime
import asyncio

from app.models.order import Order, OrderStatus
from app.rabbitmq import send_to_document_queue
from app.repositories.db_order_repo import OrderRepo
from app.repositories.local_order_repo import OrderRepo

from app.services.document_service import DocumentService


class OrderService():
    order_repo: OrderRepo
    document_service: DocumentService

    # deliveryman_repo: DeliverymenRepo

    def __init__(self, order_repo: OrderRepo = Depends(OrderRepo),
                 document_service: DocumentService = Depends(DocumentService)) -> None:
        self.order_repo = order_repo
        self.document_service = document_service
        # self.deliveryman_repo = DeliverymenRepo()

    def get_order(self) -> list[Order]:
        return self.order_repo.get_order()

    def create_order(self, ord_id: int, address_info: str, customer_info: str, create_date: datetime,
                     completion_date: datetime, order_info: str) -> Order:
        order = Order(ord_id=ord_id, status=OrderStatus.CREATE, address_info=address_info, customer_info=customer_info,
                      create_date=create_date, completion_date=completion_date, order_info=order_info)
        return self.order_repo.create_order(order)

    def accepted_order(self, id: int) -> Order:
        order = self.order_repo.get_order_by_id(id)
        if order.status != OrderStatus.CREATE:
            raise ValueError

        order.status = OrderStatus.ACCEPTED
        # self.document_service.create_document(doc_id=order.ord_id, ord_id=order.ord_id, type="accepted_order",
        #                                       create_date=datetime.now(), completion_date=datetime.now(),
        #                                       doc="Accepted order document")

        test_data = {
            "doc_id": 1255,
            "ord_id": 4532,
            "type": "Test Type",
            "create_date": "2024-01-28T12:00:00",
            "completion_date": "2024-01-28T13:00:00",
            "doc": "Test Document"
        }
        #
        # send_to_queue(test_data)
        asyncio.run(send_to_document_queue(test_data))

        return self.order_repo.set_status(order)

    def pick_up_order(self, id: int) -> Order:
        order = self.order_repo.get_order_by_id(id)
        if order.status != OrderStatus.ACCEPTED:
            raise ValueError

        order.status = OrderStatus.PICK_UP
        return self.order_repo.set_status(order)

    def delivering_order(self, id: int) -> Order:
        order = self.order_repo.get_order_by_id(id)
        if order.status != OrderStatus.PICK_UP:
            raise ValueError

        order.status = OrderStatus.DELIVERING
        return self.order_repo.set_status(order)

    def delivered_order(self, id: int) -> Order:
        order = self.order_repo.get_order_by_id(id)
        if order.status != OrderStatus.DELIVERING:
            raise ValueError

        order.status = OrderStatus.DELIVERED
        return self.order_repo.set_status(order)

    def paid_order(self, id: int) -> Order:
        order = self.order_repo.get_order_by_id(id)
        if order.status != (OrderStatus.DELIVERED or OrderStatus.DELIVERING):
            raise ValueError

        order.status = OrderStatus.PAID
        return self.order_repo.set_status(order)

    def done_order(self, id: int) -> Order:
        order = self.order_repo.get_order_by_id(id)
        if order.status != OrderStatus.PAID:
            raise ValueError

        order.status = OrderStatus.DONE
        return self.order_repo.set_status(order)

    def cancel_order(self, id: int) -> Order:
        order = self.order_repo.get_order_by_id(id)
        if order.status != (OrderStatus.CREATE or OrderStatus.ACCEPTED):
            raise ValueError

        order.status = OrderStatus.CANCELLED
        return self.order_repo.set_status(order)

    def delete_order(self, id: int) -> None:
        order = self.order_repo.get_order_by_id(id)
        if not order:
            raise ValueError(f'Order with id={id} not found')

        return self.order_repo.delete_order(id)
