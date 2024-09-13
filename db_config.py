from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker


class Base(DeclarativeBase):
    pass


engine = create_engine(
    "postgresql+psycopg2://user:pass@localhost:5432/delivery"
)  # Substitua pela sua string de conexão
Session = scoped_session(sessionmaker(bind=engine))
db_session = Session

db = SQLAlchemy(model_class=Base)
mongo_client = MongoClient("mongodb://user:pass@localhost:27017")
mongo = mongo_client["delivery"]
