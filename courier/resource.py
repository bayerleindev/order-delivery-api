from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Api, Resource, reqparse
from courier.usecases.accept_or_reject_order import AcceptOrRejectOrder

from courier.usecases.create_courier import CreateCourier


class CourierList(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument("name", required=True, type=str, help="Name is required")
    parser.add_argument("last_name", required=True, type=str, help="Name is required")
    parser.add_argument("email", required=True, type=str, help="Email is required")
    parser.add_argument(
        "document", required=True, type=str, help="Document is required"
    )
    parser.add_argument(
        "password", required=True, type=str, help="Password is required"
    )

    def post(self):
        args = self.parser.parse_args(strict=True)

        return CreateCourier().execute(**args).to_json(), 201


class CourierOrders(Resource):

    @jwt_required()
    def patch(self):
        body = request.get_json()
        AcceptOrRejectOrder().execute(
            order_number=body["order_number"],
            status=body["status"],
            courier_id=get_jwt_identity(),
        )
        pass


def init(api: Api):
    api.add_resource(CourierList, "/couriers")
    api.add_resource(CourierOrders, "/couriers/orders")
