from typing import List
from order.model import Item, OrderHistoryModel, OrderModel

from db_config import mongo, db_session


class OrderRepository:

    def set_selected_courier(self, order_number: str, courier_id: str):
        db_session.query(OrderModel).filter(OrderModel.number == order_number).update(
            {OrderModel.selected_courier: courier_id}
        )

    def assign_couriers(self, order_number: str, courier_ids: List[str]):
        db_session.query(OrderModel).filter(OrderModel.number == order_number).update(
            {OrderModel.couriers: courier_ids}
        )
        db_session.commit()

    def update(self, order: OrderModel):
        mongo.orders.update_one(
            {"_id": order.number}, {"$set": {"status": order.status}}
        )

    def load(self, number: str):
        return mongo.orders.find_one({"_id": number})

    def filter(self, **kwargs):
        return db_session.query(OrderModel).filter_by(**kwargs)

    def save_history(self, hisotry: OrderHistoryModel):
        db_session.add(hisotry)

    def save(self, order: OrderModel):
        db_session.add(order)

        items = []
        for item in order.items:
            db_item = (
                db_session.query(Item).filter(Item.sku == item["sku"]).first().to_json()
            )
            items.append({**db_item, "amount": item["amount"]})

        mongo.orders.insert_one(
            {
                "_id": order.number,
                "number": order.number,
                "status": order.status,
                "consumer": str(order.consumer_id),
                "seller": str(order.seller_id),
                "address": order.address,
                "items": items,
            }
        )

        return mongo.orders.find_one({"_id": order.number})
