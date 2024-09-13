from typing import List
from uuid import UUID
from auth.model import AuthModel, Role
from db_config import db


class Auth:
    def register(self, email: str, password: str, identity_id: UUID, roles: List[Role]):
        user = AuthModel(
            email=email, password=password, identity_id=identity_id, roles=roles
        )
        db.session.add(user)

    def login(self, email: str, password: str):
        return (
            db.session.query(AuthModel)
            .filter(AuthModel.email == email)
            .filter(AuthModel.password == password)
            .filter(AuthModel.is_operational)
            .first()
        )
