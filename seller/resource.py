from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Api, Resource, abort
from seller.exception import SellerException

from seller.service import SellerService

service = SellerService()


class Seller(Resource):
    pass


class SellerList(Resource):
    def post(self):
        try:
            body = request.get_json()
            return service.save(**body).to_json()
        except SellerException as e:
            abort(500, message=e.message)

    def get(self):
        return service.get_sellers()


class ItemsList(Resource):
    @jwt_required()
    def post(self):
        service.save_item(get_jwt_identity(), items=request.get_json())
        return {}, 201

    @jwt_required(optional=True)
    def get(self, id: str = None):
        if not id:
            return service.get_items(get_jwt_identity())
        return service.get_items(id)


class SellerOrders(Resource):
    @jwt_required()
    def patch(self, order_number: str):
        status = request.get_json()["status"]
        service.accept_or_reject_order(get_jwt_identity(), order_number, status)

    @jwt_required()
    def get(self):
        try:
            identity = get_jwt_identity()
            return service.get_orders(identity)
        except Exception as e:
            print(e)
        abort(403)


def init(api: Api):
    api.add_resource(SellerList, "/sellers/")
    api.add_resource(
        SellerOrders, "/sellers/orders/", "/sellers/orders/<string:order_number>"
    )
    api.add_resource(ItemsList, "/items", "/sellers/<string:id>/items")
