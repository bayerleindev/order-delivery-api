from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Api, Resource
from courier.usecases.accept_or_reject_order import AcceptOrRejectOrder

from courier.usecases.create_courier import CreateCourier


class CourierList(Resource):
    def post(self):
        args = request.get_json()
        return CreateCourier().execute(**args).to_json(), 201


class CourierOrders(Resource):

    @jwt_required()
    def patch(self):
        body = request.get_json()
        return (
            AcceptOrRejectOrder()
            .execute(
                order_number=body["order_number"],
                status=body["status"],
                courier_id=get_jwt_identity(),
            )
            .to_json(),
            200,
        )


def init(api: Api):
    api.add_resource(CourierList, "/couriers")
    api.add_resource(CourierOrders, "/couriers/orders")
