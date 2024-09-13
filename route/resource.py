from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Api, Resource, abort, reqparse
from order.exception import OrderException
from route.exception import RouteException


from route.service import RouteService

service = RouteService()


class Route(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("status", required=True, type=str, help="Status is required")
    parser.add_argument("courier", location="headers", type=str)

    @jwt_required()
    def get(self, id=None):
        courier = get_jwt_identity()
        return service.get_latest_route(courier).to_json(), 200

    @jwt_required()
    def patch(self):
        try:
            args = self.parser.parse_args(strict=True)
            args["courier"] = get_jwt_identity()
            return service.update_status(**args).to_json(), 200
        except RouteException as e:
            abort(500, message=e.message)
        except OrderException as e:
            abort(500, message=e.message)
        finally:
            print("========== LOG ==========")


class RouteOrders(Resource):
    @jwt_required()
    def post(self):
        try:
            body = request.get_json()
            return service.add_order_to_active_route(
                get_jwt_identity(), body["order"]
            ).to_json()
        except RouteException as e:
            abort(500, message=e.message)
        except OrderException as e:
            abort(500, message=e.message)
        finally:
            print("========== LOG ==========")


class RouteList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "order", required=True, type=str, help="Order number is required"
    )

    @jwt_required()
    def post(self, id):
        args = self.parser.parse_args(strict=True)
        try:
            return service.add_order_to_active_route(
                id, get_jwt_identity(), args["order"]
            ).to_json()
        except RouteException as e:
            abort(500, message=e.message)
        except OrderException as e:
            abort(500, message=e.message)
        finally:
            print("========== LOG ==========")

    @jwt_required()
    def delete(self, id):
        args = self.parser.parse_args(strict=True)
        try:
            return service.remove_order(id, args["order"]).to_json()
        except RouteException as e:
            abort(500, message=e.message)
        finally:
            print("========== LOG ==========")


def init(api: Api):
    api.add_resource(Route, "/routes/<string:id>", "/routes/")
    # api.add_resource(RouteList, '/routes/<string:id>/orders')
    api.add_resource(RouteOrders, "/routes/orders")
