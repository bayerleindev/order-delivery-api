from seller.model import SellerModel
from seller.repository import SellerRepository


class CreateSeller:

    def __init__(self) -> None:
        self.repository = SellerRepository()

    def execute(self, **kwargs) -> SellerModel:
        seller = SellerModel(document=kwargs["document"], name=kwargs["name"])
        self.repository.add_seller(seller)

        return seller
