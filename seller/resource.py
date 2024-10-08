from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Api, Resource, abort
from seller.exception import SellerException

from seller.usecases.accept_or_reject_order import AcceptOrRejectOrder
from seller.usecases.create_seller import CreateSeller
from seller.usecases.get_items import GetItems
from seller.usecases.get_orders import GetOrders
from seller.usecases.filter_sellers import FilterSellers
from seller.usecases.save_item import SaveItem


class Seller(Resource):
    pass


class SellerList(Resource):
    def post(self):
        body = request.get_json()
        return (
            CreateSeller().execute(**body).to_json(),
            201,
        )

    def get(self):
        args = request.args
        kwargs = {}
        for k, v in args.items():
            kwargs.update({k: v})
        return FilterSellers().execute(**kwargs)


class ItemsList(Resource):
    @jwt_required()
    def post(self):
        return SaveItem().execute(get_jwt_identity(), items=request.get_json()), 201

    @jwt_required(optional=True)
    def get(self, id: str = None):
        return GetItems().execute(seller_id=id or get_jwt_identity())


class SellerOrders(Resource):
    @jwt_required()
    def patch(self, order_number: str):
        try:
            status = request.get_json()["status"]
            result = AcceptOrRejectOrder().execute(
                seller_id=get_jwt_identity(),
                status=status,
                order_number=order_number,
            )
            return result, 201
        except SellerException as error:
            abort(500, message=error.message)

    @jwt_required()
    def get(self):
        return GetOrders().execute(seller_id=get_jwt_identity())


def init(api: Api):
    api.add_resource(SellerList, "/sellers/")
    api.add_resource(
        SellerOrders, "/sellers/orders/", "/sellers/orders/<string:order_number>"
    )
    api.add_resource(ItemsList, "/items", "/sellers/<string:id>/items")
