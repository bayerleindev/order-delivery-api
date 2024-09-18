from flask import request
from flask_restful import Api, Resource
from geolocation.usecases.get_order_location import GetOrderGeolocation

from geolocation.usecases.save_geolocation import SaveGeolocation


class CourierGeolocation(Resource):

    def post(self):
        data = request.get_json()
        SaveGeolocation().execute(**data)


class OrderGeolocation(Resource):

    def get(self, order_number: str):
        return GetOrderGeolocation().execute(order_number)


def init(api: Api):
    api.add_resource(CourierGeolocation, "/geolocations")
    api.add_resource(OrderGeolocation, "/geolocations/<string:order_number>")
