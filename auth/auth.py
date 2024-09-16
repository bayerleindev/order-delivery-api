import json
import os
from uuid import UUID
import requests


class Auth:
    def register(self, email: str, password: str, name: str, last_name: str, id: UUID):
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

        return requests.post(
            "http://127.0.0.1:8080/admin/realms/master/users",
            headers={"Authorization": "Bearer {}".format(admin_token)},
            data=json.dumps(data),
        )

    def login(self, email: str, password: str):

        data = {
            "client_id": os.environ.get("KEYCLOAK_CLIENT_ID"),
            "grant_type": "password",
            "username": email,
            "password": password,
        }

        request = requests.post(
            "http://127.0.0.1:8080/realms/master/protocol/openid-connect/token",
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
            "http://127.0.0.1:8080/realms/master/protocol/openid-connect/token",
            data=body,
            timeout=10,
        ).json()

        return json

    def get_user_info(self, email: str):
        return requests.get(
            "http://127.0.0.1:8080/admin/realms/master/users?email={}".format(email),
            headers={
                "Authorization": "Bearer {}".format(
                    self.get_admin_token().get("access_token")
                )
            },
        )
