from commons.scheduler import schedule
from courier.usecases.assign_order_to_courier import AssignOrderToCourier
from order.usecases.filter_order import FilterOrder
from order.usecases.update_order import Input, UpdateOrder
from seller.exception import SellerException
from seller.repository import SellerRepository


class AcceptOrRejectOrder:

    def __init__(self) -> None:
        self.accepted_status = ["ACCEPTED", "REJECTED"]
        self.repository = SellerRepository()

    def __print(self, txt: str):
        print(txt)

    def execute(self, **kwargs):
        seller_id = kwargs["seller_id"]
        order_number = kwargs["order_number"]
        status = kwargs["status"]

        if status not in self.accepted_status:
            raise SellerException("Status {} not allowed".format(status))

        order = FilterOrder().execute(number=order_number).first()

        if not order or str(order.seller_id) != str(seller_id):
            raise SellerException("Order {} not found.".format(order_number))

        result = UpdateOrder().execute(Input(order_number, status))

        if not order.selected_courier:
            seller = self.repository.get_sellers(id=seller_id)[0]

            schedule(
                AssignOrderToCourier().execute,
                5,
                [seller.longitude, seller.latitude],
                order_number,
            )
        return result
