import datetime
from flask import request
from flask_jwt_extended import create_access_token
from flask_restful import Api, Resource, reqparse

from auth.auth import Auth
from commons.base_exception import CustomBaseException
from commons.errors import ERROR_MESSAGES

auth = Auth()


class SendConfirmationCode(Resource):
    def post(self):
        return auth.send_confirmation_email(request.get_json()["email"]), 201


class ConfirmationCode(Resource):
    def post(self):
        body = request.get_json()
        return auth.verify_confirmation_code(body["email"], body["confirmation_code"])


class Login(Resource):
    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument("email", required=True, type=str, help="Email is required")
        parser.add_argument(
            "password", required=True, type=str, help="Password is required"
        )
        args = parser.parse_args(strict=True)

        login = auth.login(args["email"], args["password"])

        if not login or not login.ok or not bool(login.json()[0].get("emailVerified")):
            raise CustomBaseException(ERROR_MESSAGES["EMAIL_NOT_VERIFIED"]["pt"])

        if login.ok:
            id = login.json()[0].get("attributes").get("id")[0]

            access_token = create_access_token(
                identity=id,
                additional_claims={"id": id},
                expires_delta=datetime.timedelta(minutes=15),
            )

        return {"access_token": access_token}, 201


def init(api: Api):
    api.add_resource(Login, "/login")
    api.add_resource(ConfirmationCode, "/confirm-email")
    api.add_resource(SendConfirmationCode, "/send-confirmation-code")
