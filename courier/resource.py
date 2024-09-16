from flask_restful import Api, Resource, reqparse

from courier.service import CourierService

service = CourierService()


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
        return service.save(**args), 201

    def get(self):
        return service.get_all()


def init(api: Api):
    api.add_resource(CourierList, "/couriers")
