import datetime
from flask_jwt_extended import create_access_token
from flask_restful import Api, Resource, reqparse

from auth.auth import Auth

auth = Auth()


class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("email", required=True, type=str, help="Email is required")
        parser.add_argument(
            "password", required=True, type=str, help="Password is required"
        )
        args = parser.parse_args(strict=True)

        courier = auth.login(args["email"], args["password"])

        if courier:
            access_token = create_access_token(
                identity=courier.identity_id,
                additional_claims={"id": courier.identity_id},
                expires_delta=datetime.timedelta(minutes=15),
            )
            return {"access_token": access_token}, 201
        return {}, 403


def init(api: Api):
    api.add_resource(Login, "/login")
