from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Api, Resource, abort, reqparse
from commons.decorators import check_order_in_route
from commons.logger import Logger
from order.exception import OrderException


from order.usecases.create_order import CreateOrder, Input
from order.usecases.filter_order import FilterOrder
from order.usecases.update_order import UpdateOrder, Input as UpdateInput
from order.usecases.load_order import LoadOrder


logger = Logger(__name__)


class OrderList(Resource):
    @jwt_required()
    def post(self):
        try:
            body = request.get_json()
            consumer = get_jwt_identity()
            order = CreateOrder().execute(
                input=Input(
                    body.get("seller_id"),
                    consumer,
                    body.get("items"),
                    body.get("shipping_address"),
                )
            )
            return order, 201
        except OrderException as error:
            abort(500, message=error.message)
        finally:
            logger.info("Remain calm! %s", consumer)


class Order(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("status", required=True, type=str, help="Status is required")
    parser.add_argument("latitude", location="headers", type=str)
    parser.add_argument("longitude", location="headers", type=str)

    @jwt_required()
    def get(self, number: str):
        identity = get_jwt_identity()
        order = FilterOrder().execute(consumer_id=identity, number=number).first()
        if order:
            return LoadOrder().execute(number), 200
        abort(404, message="Order not found.")

    @jwt_required()
    @check_order_in_route
    def patch(self, number):
        try:
            args = self.parser.parse_args(strict=True)
            # order = service.update_status(number, **args)
            order = UpdateOrder().execute(UpdateInput(number, args.get("status")))
            return order, 200
        except OrderException as e:
            abort(500, message=e.message)
        finally:
            print("========== LOG ==========")


def init(api: Api):
    api.add_resource(Order, "/orders/<string:number>")
    api.add_resource(OrderList, "/orders")
