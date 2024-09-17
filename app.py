from flask import Flask, Response
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from middlewares.after_request_handler import AfterRequestHandler
from middlewares.before_request_handler import BeforeRequestHandler
from order import resource as order_resource
from courier import resource as courier_resource
from route import resource as route_resource
from auth import resource as auth_resource
from seller import resource as seller_resource
from consumer import resource as consumer_resource
from geolocation import resource as geolocation_resource
from db_config import db
from flask_migrate import Migrate


errors = {
    "ExpiredSignatureError": {
        "message": "Token Expired",
        "status": 401,
    },
}

app = Flask(__name__)
api = Api(app, errors=errors)
migrate = Migrate()
jwt = JWTManager(app)
cors = CORS(app)

app.config["CORS_HEADERS"] = "Content-Type"
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/delivery"
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql+psycopg2://user:pass@127.0.0.1:5432/delivery"
)


@app.before_request
def before_request_callback():
    BeforeRequestHandler.handle()


@app.after_request
def after_request_callback(response: Response):
    AfterRequestHandler.handle(response)
    return response


db.init_app(app)
migrate.init_app(app, db)

order_resource.init(api)
courier_resource.init(api)
route_resource.init(api)
auth_resource.init(api)
seller_resource.init(api)
consumer_resource.init(api)
geolocation_resource.init(api)
