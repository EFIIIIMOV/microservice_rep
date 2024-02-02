import enum
from uuid import UUID
from datetime import datetime
from pydantic import ConfigDict, BaseModel


class OrderStatus(enum.Enum):
    CREATE = 'create'
    ACCEPTED = 'accepted'
    PICK_UP = 'pick_up'
    DELIVERING = 'delivering'
    DELIVERED = 'delivered'
    PAID = 'paid'
    DONE = 'done'
    CANCELLED = 'cancelled'


class Order(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    # ord_id: UUID
    ord_id: int
    status: OrderStatus
    address_info: str
    customer_info: str
    create_date: datetime
    completion_date: datetime
    order_info: str


class CreateOrderRequest(BaseModel):
    # ord_id: UUID
    ord_id: int
    address_info: str
    customer_info: str
    create_date: datetime
    completion_date: datetime
    order_info: str
