from auth.auth import Auth
from commons.base_exception import CustomBaseException
from commons.errors import get_error
from commons.logger import Logger
from seller.model import SellerModel
from seller.repository import SellerRepository

logger = Logger(__name__)


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
        raise CustomBaseException(get_error("USER_EXISTS"))
