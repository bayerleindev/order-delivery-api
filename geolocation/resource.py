from flask import request
from flask_restful import Api, Resource

from geolocation.usecases.save_geolocation import SaveGeolocation


class CourierGeolocation(Resource):

    def post(self):
        data = request.get_json()
        SaveGeolocation().execute(**data)


def init(api: Api):
    api.add_resource(CourierGeolocation, "/geolocations")
