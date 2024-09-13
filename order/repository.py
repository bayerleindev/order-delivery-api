from order.model import Item, OrderHistoryModel, OrderModel

from db_config import db, mongo


class OrderRepository:
    def update(self, order: OrderModel):
        mongo.orders.update_one(
            {"_id": order.number}, {"$set": {"status": order.status}}
        )

    def load(self, number: str):
        return mongo.orders.find_one({"_id": number})

    def filter(self, **kwargs):
        return db.session.query(OrderModel).filter_by(**kwargs)

    def save_history(self, hisotry: OrderHistoryModel):
        db.session.add(hisotry)
        self.commit()

    def save(self, order: OrderModel):
        db.session.add(order)

        items = []
        for item in order.items:
            db_item = (
                db.session.query(Item).filter(Item.sku == item["sku"]).first().to_json()
            )
            items.append({**db_item, "amount": item["amount"]})

        mongo.orders.insert_one(
            {
                "_id": order.number,
                "number": order.number,
                "status": order.status,
                "consumer": order.consumer_id,
                "address": order.address,
                "items": items,
            }
        )

        self.commit()

        return mongo.orders.find_one({"_id": order.number})

    def commit(self):
        db.session.commit()
