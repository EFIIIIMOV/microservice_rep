import traceback
from uuid import UUID
from sqlalchemy.orm import Session

from app_order.app.database import get_db_ord
from app_order.app.models.order import Order
from app_order.app.schemas.order import Order as DBOrder


class OrderRepo():
    db: Session

    def __init__(self) -> None:
        self.db = next(get_db_ord())

    def _map_to_model(self, order: DBOrder) -> Order:
        result = Order.from_orm(order)

        return result

    def _map_to_schema(self, order: Order) -> DBOrder:
        data = dict(order)
        result = DBOrder(**data)

        return result

    def get_order(self) -> list[Order]:
        orders = []
        for d in self.db.query(DBOrder).all():
            orders.append(self._map_to_model(d))

        return orders

    def get_order_by_id(self, id: UUID) -> Order:
        order = self.db \
            .query(DBOrder) \
            .filter(DBOrder.ord_id == id) \
            .first()

        if order == None:
            raise KeyError
        return self._map_to_model(order)

    def create_order(self, order: Order) -> Order:
        try:
            db_order = self._map_to_schema(order)
            self.db.add(db_order)
            self.db.commit()
            return self._map_to_model(db_order)
        except:
            traceback.print_exc()
            raise KeyError

    def set_status(self, order: Order) -> Order:
        db_order = self.db.query(DBOrder).filter(
            DBOrder.ord_id == order.ord_id).first()
        db_order.status = order.status
        db_order.completion_date = order.completion_date
        self.db.commit()
        return self._map_to_model(db_order)

    def delete_all_orders(self) -> None:
        try:
            # Delete all orders from the database
            self.db.query(DBOrder).delete()
            self.db.commit()
        except Exception as e:
            print(f"An error occurred while deleting all orders: {e}")
            self.db.rollback()
            raise
