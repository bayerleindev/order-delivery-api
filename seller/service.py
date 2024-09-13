from datetime import datetime, timedelta
from uuid import UUID
from sqlalchemy.exc import IntegrityError

from auth.model import AuthModel, Role
from order.model import Item, OrderModel
from order.usecases.filter_order import FilterOrder
from order.usecases.load_order import LoadOrder
from order.usecases.update_order import Input, UpdateOrder
from seller.exception import SellerException
from seller.model import SellerModel
from db_config import db


class SellerService:
    def get_sellers(self):
        return [seller.to_json() for seller in db.session.query(SellerModel).all()]

    def get_orders(self, id: str):
        orders = [
            LoadOrder().execute(order.number)
            for order in FilterOrder()
            .execute(seller_id=id)
            .filter(OrderModel.created_at >= datetime.now() - timedelta(hours=2))
            .filter(OrderModel.created_at <= datetime.now())
            .order_by(OrderModel.created_at.desc())
            .all()
        ]
        result = {"pending": [], "in_transit": [], "finalized": [], "accepted": []}
        for order in orders:
            if order["status"] == "ACCEPTED" or order["status"] == "CONFIRMED":
                result["accepted"].append(order)
            elif order["status"] == "PENDING":
                result["pending"].append(order)
            elif (
                order["status"] == "ARRIVED"
                or order["status"] == "IN_TRANSIT"
                or order["status"] == "ORDER_IN_TRANSIT"
            ):
                result["in_transit"].append(order)
            else:
                result["finalized"].append(order)
        return result

    def accept_or_reject_order(self, id: str, order_number: str, status: str):
        UpdateOrder().execute(Input(order_number, status))

    def save(self, **kwargs):
        try:
            with db.session.begin():
                seller = SellerModel(document=kwargs["document"], name=kwargs["name"])
                db.session.add(seller)

                user = AuthModel(
                    email=kwargs["email"],
                    password=kwargs["password"],
                    identity_id=seller.id,
                    roles=[Role.SELLER.value],
                )
                db.session.add(user)
            db.session.commit()
            db.session.refresh(seller)
            db.session.close()

            return seller
        except IntegrityError as e:
            print(e)
            raise SellerException("Seller already exists.")

    def get_items(self, id: UUID):
        return [
            item.to_json()
            for item in db.session.query(Item).filter(Item.seller_id == id).all()
        ]
