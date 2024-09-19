from uuid import UUID
from flask import request
from flask_restful import Api, Resource, abort
from consumer.exception import ConsumerException
from consumer.usecases.create_user import CreateUser
from order.usecases.filter_order import FilterOrder
from order.usecases.load_order import LoadOrder


class ConsumerList(Resource):
    def post(self):
        try:
            body = request.get_json()
            consumer = CreateUser().execute(
                document=body.get("document"),
                name=body.get("name"),
                email=body.get("email"),
                phone=body.get("phone"),
                password=body.get("password"),
                last_name=body.get("last_name"),
            )

            return consumer.to_json(), 201
        except ConsumerException as error:
            abort(500, error=error.error)


class ConsumerOrders(Resource):

    def get(self, consumer_id: UUID):
        return [
            LoadOrder().execute(order.number)
            for order in FilterOrder().execute(consumer_id=consumer_id)
        ]


def init(api: Api):
    api.add_resource(ConsumerOrders, "/consumers/<string:consumer_id>/orders")
    api.add_resource(ConsumerList, "/consumers/")
