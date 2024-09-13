from typing import List
from order.model import Item
from db_config import db_session
from seller.model import SellerModel


class SellerRepository:

    def add_seller(self, seller: SellerModel):
        db_session.add(seller)

    def get_sellers(self, **kwargs):
        if kwargs:
            return db_session.query(SellerModel).filter_by(**kwargs).all()
        return []

    def save_all_items(self, items: List[Item]):
        db_session.add_all(items)

    def get_items(self, **kwargs):
        return db_session.query(Item).filter_by(**kwargs).all()
