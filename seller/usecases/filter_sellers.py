from seller.usecases.repository import SellerRepository


class FilterSellers:

    def __init__(self) -> None:
        self.repository = SellerRepository()

    def execute(self, **kwargs):
        sellers = self.repository.get_sellers(**kwargs)
        return [seller.to_json() for seller in sellers]
