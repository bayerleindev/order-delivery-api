from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
mongo_client = MongoClient("mongodb://user:pass@localhost:27017")
mongo = mongo_client["delivery"]
