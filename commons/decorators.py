import functools

from flask import request
from flask_restful import abort
from flask_jwt_extended import get_jwt_identity

from route.usecases.get_route import GetRoute
from route.usecases.get_route_orders import GetRouteOrders

def check_order_in_route(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        courier = get_jwt_identity()
        route = GetRoute().execute(courier_id=courier)
        order = request.view_args["number"]
        if not route:
            abort(
                404, message="Order not found in your route. Make sure you have added."
            )
        if order not in [
            order.order_number for order in GetRouteOrders().execute(route_id=route.id)
        ]:
            abort(
                404, message="Order not found in your route. Make sure you have added."
            )
        return func(*args, **kwargs)

    return wrapper
