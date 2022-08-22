import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy import Integer


# Initializes default app config values
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
Base = declarative_base()


# Blueprint for the User Class
class User(UserMixin, db.Model, Base):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    flights = relationship("FlightData", back_populates="user")


# Blueprint for the Flight Data Class
class FlightData(db.Model, Base):
    __tablename__ = "flightdata"
    id = db.Column(db.Integer, primary_key=True)
    to_city = db.Column(db.String(50))
    from_city = db.Column(db.String(50))
    to_iata_code = db.Column(db.String(10))
    from_iata_code = db.Column(db.String(10))
    from_date = db.Column(db.String)
    to_date = db.Column(db.String)
    price = db.Column(db.Integer)
    url = db.Column(db.String)
    user_id = db.Column(Integer, db.ForeignKey("user.id"))
    user = relationship("User", back_populates='flights')

