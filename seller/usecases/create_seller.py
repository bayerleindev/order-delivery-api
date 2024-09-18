from auth.auth import Auth
from seller.model import SellerModel
from seller.repository import SellerRepository


class CreateSeller:

    def __init__(self) -> None:
        self.repository = SellerRepository()

    def execute(self, **kwargs) -> SellerModel:
        seller = SellerModel(
            document=kwargs["document"],
            name=kwargs["name"],
            latitude=kwargs["latitude"],
            longitude=kwargs["longitude"],
        )

        identity = Auth().register(
            kwargs["email"],
            kwargs["password"],
            name=kwargs["name"],
            last_name=kwargs["name"],
            id=seller.id,
        )

        if identity.ok:
            self.repository.add_seller(seller)
            return seller
        return identity.json()
