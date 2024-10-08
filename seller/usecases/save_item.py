from uuid import UUID

from order.model import Item
from seller.repository import SellerRepository


class SaveItem:

    def __init__(self) -> None:
        self.repository = SellerRepository()

    def execute(self, seller_id: UUID, **kwargs):
        items = [Item(seller_id=seller_id, **item) for item in kwargs["items"]]
        self.repository.save_all_items(items)
        return [item.to_json() for item in items]
