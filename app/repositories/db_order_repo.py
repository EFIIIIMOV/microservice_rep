import traceback
from uuid import UUID
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.order import Order
from app.schemas.order import Order as DBOrder


# from app.repositories.local_deliveryman_repo import DeliverymenRepo


class OrderRepo():
    db: Session

    # deliveryman_repo: DeliverymenRepo

    def __init__(self) -> None:
        self.db = next(get_db())
        # self.deliveryman_repo = DeliverymenRepo()

    def _map_to_model(self, order: DBOrder) -> Order:
        result = Order.from_orm(order)
        # if order.deliveryman_id != None:
        #     result.deliveryman = self.deliveryman_repo.get_deliveryman_by_id(
        #         order.deliveryman_id)

        return result

    def _map_to_schema(self, order: Order) -> DBOrder:
        data = dict(order)
        # del data['deliveryman']
        # data['deliveryman_id'] = order.deliveryman.id if order.deliveryman != None else None
        result = DBOrder(**data)

        return result

    def get_order(self) -> list[Order]:
        orders = []
        for d in self.db.query(DBOrder).all():
            orders.append(self._map_to_model(d))
        return orders

    # def get_order_by_id(self, id: UUID) -> Order:
    #     order = self.db \
    #         .query(DBOrder) \
    #         .filter(DBOrder.id == id) \
    #         .first()
    #
    #     if order == None:
    #         raise KeyError
    #     return self._map_to_model(order)

    def get_order_by_id(self, id: int) -> Order:
        order = self.db \
            .query(DBOrder) \
            .filter(DBOrder.id == id) \
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
            DBOrder.id == order.id).first()
        db_order.status = order.status
        self.db.commit()
        return self._map_to_model(db_order)

    # def delete_order(self, order_id: UUID) -> None:
    #     order = self.db.query(DBOrder).filter(DBOrder.id == order_id).first()
    #     if order:
    #         self.db.delete(order)
    #         self.db.commit()
    #     else:
    #         raise KeyError("Order not found")

    def delete_order(self, order_id: int) -> None:
        order = self.db.query(DBOrder).filter(DBOrder.id == order_id).first()
        if order:
            self.db.delete(order)
            self.db.commit()
        else:
            raise KeyError("Order not found")
