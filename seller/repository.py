from typing import List
from order.model import Item
from db_config import db
from seller.model import SellerModel


class SellerRepository:

    def add_seller(self, seller: SellerModel):
        db.session.add(seller)
        db.session.commit()

    def get_sellers(self, **kwargs):
        if kwargs:
            return db.session.query(SellerModel).filter_by(**kwargs).all()
        return []

    def save_all_items(self, items: List[Item]):
        db.session.add_all(items)
        db.session.commit()

    def get_items(self, **kwargs):
        return db.session.query(Item).filter_by(**kwargs).all()
