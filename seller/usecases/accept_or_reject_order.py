from order.usecases.filter_order import FilterOrder
from order.usecases.update_order import Input, UpdateOrder
from seller.exception import SellerException


class AcceptOrRejectOrder:

    def __init__(self) -> None:
        self.accepted_status = ["ACCEPTED", "REJECTED"]

    def execute(self, **kwargs):
        seller_id = kwargs["seller_id"]
        order_number = kwargs["order_number"]
        status = kwargs["status"]

        if status not in self.accepted_status:
            raise SellerException("Status {} not allowed".format(status))

        order = FilterOrder().execute(number=order_number).first()

        if not order or str(order.seller_id) != str(seller_id):
            raise SellerException("Order {} not found.".format(order_number))

        return UpdateOrder().execute(Input(order_number, status))

    # TODO delegate order to courier
