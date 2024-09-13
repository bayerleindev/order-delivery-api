from seller.repository import SellerRepository


class GetItems:
    def __init__(self) -> None:
        self.repository = SellerRepository()

    def execute(self, **kwargs):
        return [item.to_json() for item in self.repository.get_items(**kwargs)]
