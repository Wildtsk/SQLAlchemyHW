from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Text, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from utils import get_users_all, get_orders_all, get_offers_all

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URL"] = "sqlite:///job_db"

db = SQLAlchemy(app)


class Offer(db.Model):
    __tablename__ = "offer"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order.id'))
    executor_id = Column(Integer, ForeignKey('user.id'))

    order = relationship("Order")
    user = relationship("User")


class Order(db.Model):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(Text)
    start_date = Column(Date)
    end_date = Column(Date)
    address = Column(Text)
    price = Column(Integer)
    customer_id = Column(Integer, ForeignKey('user.id'))
    executor_id = Column(Integer, ForeignKey('user.id'))

    user = relationship("User")
    offers = relationship("Offer")


class User(db.Model):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    age = Column(Integer)
    email = Column(Text)
    role = Column(Text)
    phone = Column(Text)

    order_customer = relationship('Order')
    order_executor = relationship('Order')
    offers = relationship("Offer")


db.create_all()


users_dict = [User(**meaning) for meaning in get_users_all()]
orders_dict = [User(**meaning) for meaning in get_orders_all()]
offers_dict = [User(**meaning) for meaning in get_offers_all()]

with db.session.begin():
    db.session.add_all(users_dict)
    db.session.add_all(orders_dict)
    db.session.add_all(offers_dict)

db.session.commit()


if __name__ == "__main__":
    app.run(debug=True)