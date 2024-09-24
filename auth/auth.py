import json
import os
from uuid import UUID
import requests

from commons.base_exception import CustomBaseException
from commons.errors import ERROR_MESSAGES
from commons.random_code import generate_random_code

confirmation_code_cache = dict()


class Auth:

    def __init__(self) -> None:
        self.api_url = os.environ.get("KEYCLOAK_API_URL")

    def verify_confirmation_code(self, email: str, code: str):
        registered_code = confirmation_code_cache.get(email, "")
        if registered_code != code:
            raise CustomBaseException(ERROR_MESSAGES["WRONG_VERIFICATION_CODE"]["pt"])
        confirmation_code_cache[email] = True
        return {}

    def send_confirmation_email(self, email: str):
        user = self.get_user_info(email).json()
        if len(user) > 0:
            raise CustomBaseException(ERROR_MESSAGES["USER_EXISTS"]["pt"])

        confirmation_code = generate_random_code(size=6)
        confirmation_code_cache[email] = confirmation_code
        print("code {} sent to {}".format(confirmation_code, email))
        return {}

    def register(self, email: str, password: str, name: str, last_name: str, id: UUID):
        verified_code = confirmation_code_cache.get(email, "")
        if not verified_code:
            raise CustomBaseException(ERROR_MESSAGES["WRONG_VERIFICATION_CODE"]["pt"])
        admin_token = self.get_admin_token().get("access_token")

        data = {
            "username": email,
            "email": email,
            "firstName": name,
            "lastName": last_name,
            "enabled": True,
            "credentials": [
                {"type": "password", "value": password, "temporary": False}
            ],
            "attributes": {"id": str(id)},
        }

        response = requests.post(
            "{}/admin/realms/master/users".format(self.api_url),
            headers={"Authorization": "Bearer {}".format(admin_token)},
            data=json.dumps(data),
        )
        if response.status_code == 409:
            raise CustomBaseException(ERROR_MESSAGES["USER_EXISTS"]["pt"])

        return response

    def login(self, email: str, password: str):

        data = {
            "client_id": os.environ.get("KEYCLOAK_CLIENT_ID"),
            "grant_type": "password",
            "username": email,
            "password": password,
        }

        request = requests.post(
            "{}/realms/master/protocol/openid-connect/token".format(self.api_url),
            data=data,
        )

        if request.ok:
            return self.get_user_info(email)

    def get_admin_token(self):

        body = {
            "client_id": "admin-cli",
            "grant_type": "password",
            "username": os.environ.get("KEYCLOAK_ADMIN_USER", ""),
            "password": os.environ.get("KEYCLOAK_ADMIN_PASS", ""),
        }

        json = requests.post(
            "{}/realms/master/protocol/openid-connect/token".format(self.api_url),
            data=body,
            timeout=10,
        ).json()

        return json

    def get_user_info(self, email: str):
        return requests.get(
            "{}/admin/realms/master/users?email={}".format(self.api_url, email),
            headers={
                "Authorization": "Bearer {}".format(
                    self.get_admin_token().get("access_token")
                )
            },
        )
