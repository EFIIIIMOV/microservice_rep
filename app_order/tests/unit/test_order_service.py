import pytest
from uuid import uuid4, UUID
from datetime import datetime

from app_order.app.services.order_service import OrderService
from app_order.app.models.order import OrderStatus
from app_order.app.repositories.local_order_repo import OrderRepo


@pytest.fixture(scope='session')
def order_service() -> OrderService:
    return OrderService(OrderRepo(clear=True))


@pytest.fixture(scope='session')
def first_order_data() -> tuple[str, str, str]:
    return ('test_address_info_1', 'test_customer_info_1', 'test_order_info_1')


@pytest.fixture(scope='session')
def second_order_data() -> tuple[str, str, str]:
    return ('test_address_info_2', 'test_customer_info_2', 'test_order_info_2')


def test_empty_deliveries(order_service: OrderService) -> None:
    assert order_service.get_order() == []


def test_create_first_order(
        first_order_data: tuple[str, str, str],
        order_service: OrderService
) -> None:
    address_info, customer_info, order_info = first_order_data
    order = order_service.create_order(address_info, customer_info, order_info)
    assert order.address_info == address_info
    assert order.customer_info == customer_info
    assert order.status == OrderStatus.CREATE
    assert order.completion_date == None
    assert order.order_info == order_info


def test_create_second_order(
        second_order_data: tuple[str, str, str],
        order_service: OrderService
) -> None:
    address_info, customer_info, order_info = second_order_data
    order = order_service.create_order(address_info, customer_info, order_info)
    assert order.address_info == address_info
    assert order.customer_info == customer_info
    assert order.status == OrderStatus.CREATE
    assert order.completion_date == None
    assert order.order_info == order_info


def test_get_order_full(
        first_order_data: tuple[str, str, str],
        second_order_data: tuple[str, str, str],
        order_service: OrderService
) -> None:
    orders = order_service.get_order()
    assert len(orders) == 2
    assert orders[0].address_info == first_order_data[0]
    assert orders[1].address_info == second_order_data[0]


def test_done_order_status_error(
        first_order_data: tuple[str, str, str],
        order_service: OrderService
) -> None:
    with pytest.raises(ValueError):
        orders = order_service.get_order()
        order_service.done_order(orders[0].ord_id)


def test_done_order_not_found(
        order_service: OrderService
) -> None:
    with pytest.raises(KeyError):
        order_service.done_order(uuid4())


def test_done_order_status_error(
        second_order_data: tuple[str, str, str],
        order_service: OrderService
) -> None:
    with pytest.raises(ValueError):
        orders = order_service.get_order()
        order_service.done_order(orders[1].ord_id)


def test_accepted_order_not_found(
        order_service: OrderService
) -> None:
    with pytest.raises(KeyError):
        order_service.accepted_order(uuid4())

#
# def test_activate_delivery(
#         first_delivery_data: tuple[UUID, str, datetime],
#         delivery_service: DeliveryService
# ) -> None:
#     delivery = delivery_service.activate_delivery(first_delivery_data[0])
#     assert delivery.status == DeliveryStatuses.ACTIVATED
#     assert delivery.id == first_delivery_data[0]
#
#
# def test_set_deliveryman(
#         first_delivery_data: tuple[UUID, str, datetime],
#         delivery_service: DeliveryService,
#         deliveryman_repo: DeliverymenRepo
# ) -> None:
#     deliveryman = deliveryman_repo.get_deliverymen()[0]
#     delivery = delivery_service.set_deliveryman(
#         first_delivery_data[0], deliveryman.id)
#     assert delivery.status == DeliveryStatuses.ACTIVATED
#     assert delivery.id == first_delivery_data[0]
#     assert delivery.deliveryman.id == deliveryman.id
#     assert delivery.deliveryman.name == deliveryman.name
#
#
# def test_change_deliveryman(
#         first_delivery_data: tuple[UUID, str, datetime],
#         delivery_service: DeliveryService,
#         deliveryman_repo: DeliverymenRepo
# ) -> None:
#     deliveryman = deliveryman_repo.get_deliverymen()[1]
#     delivery = delivery_service.set_deliveryman(
#         first_delivery_data[0], deliveryman.id)
#     assert delivery.status == DeliveryStatuses.ACTIVATED
#     assert delivery.id == first_delivery_data[0]
#     assert delivery.deliveryman.id == deliveryman.id
#     assert delivery.deliveryman.name == deliveryman.name
#
#
# def test_finish_delivery(
#         first_delivery_data: tuple[UUID, str, datetime],
#         delivery_service: DeliveryService
# ) -> None:
#     delivery = delivery_service.finish_delivery(first_delivery_data[0])
#     assert delivery.status == DeliveryStatuses.DONE
#     assert delivery.id == first_delivery_data[0]
#
#
# def test_cancel_delivery_status_error(
#         first_delivery_data: tuple[UUID, str, datetime],
#         delivery_service: DeliveryService
# ) -> None:
#     with pytest.raises(ValueError):
#         delivery_service.cancel_delivery(first_delivery_data[0])
#
#
# def test_cancel_delivery_not_found(
#         delivery_service: DeliveryService
# ) -> None:
#     with pytest.raises(KeyError):
#         delivery_service.cancel_delivery(uuid4())
