from commons.errors import ERROR_MESSAGES
from commons.scheduler import schedule
from commons.send_email import send_email
from courier.exception import CourierException
from courier.usecases.assign_order_to_courier import AssignOrderToCourier
from order.model import OrderModel
from order.repository import OrderRepository
from order.usecases.filter_order import FilterOrder


class AcceptOrRejectOrder:
    def execute(self, **kwargs):
        order_number = kwargs["order_number"]
        courier_id = kwargs["courier_id"]
        status = kwargs["status"]

        order = FilterOrder().execute(number=order_number).first()

        if not order:
            raise CourierException(ERROR_MESSAGES["ORDER_NOT_FOUND"]["pt"])

        if status == "REJECTED":
            self.reject(order, courier_id)
        if status == "ACCEPTED":
            self.accept(order, courier_id)

        return order

    def accept(self, order: OrderModel, courier_id: str):
        OrderRepository().set_selected_courier(order.number, courier_id)

    def reject(self, order: OrderModel, courier_id: str):
        couriers = order.couriers
        couriers.remove(courier_id)

        OrderRepository().assign_couriers(order.number, couriers)
        OrderRepository().set_selected_courier(order.number, None)

        if len(couriers) > 0:

            send_email(
                "Aceitar pedido {} ? - courier {}".format(order.number, couriers[0]),
                "Novo pedido!",
            )
        else:
            schedule(
                AssignOrderToCourier().execute,
                5,
                [order.seller.longitude, order.seller.latitude],
                order.number,
            )
