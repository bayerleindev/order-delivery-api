from sqlalchemy.exc import IntegrityError

from auth.model import AuthModel, Role
from seller.exception import SellerException
from seller.model import SellerModel
from db_config import db


class SellerService:
    def get_sellers(self):
        return [seller.to_json() for seller in db.session.query(SellerModel).all()]

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
