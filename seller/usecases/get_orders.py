from datetime import datetime, timedelta
from order.model import OrderModel
from order.usecases.filter_order import FilterOrder
from order.usecases.load_order import LoadOrder


class GetOrders:
    def execute(self, **kwargs):
        id = kwargs["seller_id"]
        orders = [
            LoadOrder().execute(order.number)
            for order in FilterOrder()
            .execute(seller_id=id)
            .filter(OrderModel.created_at >= datetime.now() - timedelta(hours=2))
            .filter(OrderModel.created_at <= datetime.now())
            .order_by(OrderModel.created_at.desc())
            .all()
        ]
        result = {"pending": [], "in_transit": [], "finalized": [], "accepted": []}
        for order in orders:
            if order["status"] == "ACCEPTED" or order["status"] == "CONFIRMED":
                result["accepted"].append(order)
            elif order["status"] == "PENDING":
                result["pending"].append(order)
            elif (
                order["status"] == "ARRIVED"
                or order["status"] == "IN_TRANSIT"
                or order["status"] == "ORDER_IN_TRANSIT"
            ):
                result["in_transit"].append(order)
            else:
                result["finalized"].append(order)
        return result
