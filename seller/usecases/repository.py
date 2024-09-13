from typing import List
from order.model import Item
from db_config import db

class SellerRepository:
    def save_all_items(self, items: List[Item]):
        db.session.add_all(items)
        db.session.commit()
    
    def get_items(self, **kwargs):
        return db.session.query(Item).filter_by(**kwargs).all()