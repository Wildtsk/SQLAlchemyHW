from sqlalchemy import ForeignKey, Column, Integer, String, Text

from utils import get_users_all, get_orders_all, get_offers_all
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    """Модель пользователя"""
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String, nullable=True)
    age = Column(Integer)
    email = Column(Text)
    role = Column(Text)
    phone = Column(Text)

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone,
        }

    def __repr__(self):
        return f"User({self.id}, {self.first_name}, {self.last_name}, {self.age},{self.email},{self.role},{self.phone})"


class Order(db.Model):
    """Модель заказа"""
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(Text)
    start_date = Column(Text)
    end_date = Column(Text)
    address = Column(Text)
    price = Column(Integer)
    # Создаем внешние поля для связей между моделями
    customer_id = db.Column(db.Integer, ForeignKey("user.id"))
    executor_id = db.Column(db.Integer, ForeignKey("user.id"))
    # Создаем интерфейсы для связей, указывая каждому внешние ключи
    customer = db.relationship("User", foreign_keys=[customer_id])
    executor = db.relationship("User", foreign_keys=[executor_id])

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "address": self.address,
            "price": self.price,
        }

    def __repr__(self):
        return f"Order({self.id}, {self.name}, {self.description}, {self.start_date}, {self.end_date}, {self.address}, {self.price})"


class Offer(db.Model):
    """Модель предложения"""
    __tablename__ = 'offer'

    id = Column(Integer, primary_key=True)
    order_id = db.Column(db.Integer, ForeignKey("order.id"))
    executor_id = db.Column(db.Integer, ForeignKey("user.id"))

    order_1 = db.relationship("Order")
    user = db.relationship("User")

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id,
        }

    def __repr__(self):
        return f"Offer({self.id})"


db.drop_all()
db.create_all()

# Создаем пользователей
users = [User(**row) for row in get_users_all()]
order = [Order(**row) for row in get_orders_all()]
offer = [Offer(**row) for row in get_offers_all()]

# Загружаем все в базу данных
with db.session.begin():
    db.session.add_all(users)
    db.session.add_all(order)
    db.session.add_all(offer)

db.session.commit()

# Для проверки получаем данные из БД
order = db.session.query(Order).get(1)
offer = db.session.query(Offer).get(1)
user = db.session.query(User).get(1)


@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == "GET":
        result = []
        for us in db.session.query(User).all():
            result.append(us.to_dict())
        return jsonify(result), 200
    elif request.method == "POST":
        content = request.json
        user_add_all = [User(**row) for row in content]
        db.session.add(user_add_all)
        db.session.commit()

        result = []
        for us in db.session.query(User).all():
            result.append(us.to_dict())
        return jsonify(result), 200


@app.route('/users/<int:pk>', methods=['GET'])
def read_user(pk):
    return f'{db.session.query(User).get(pk)}'


@app.route('/orders', methods=["GET", "POST"])
def orders():
    if request.method == "GET":
        result = []
        for order_1 in db.session.query(Order).all():
            result.append(order_1.to_dict())
        return jsonify(result), 200
    elif request.method == "POST":
        content = request.json
        order_add_all = [Order(**row) for row in content]
        db.session.add(order_add_all)
        db.session.commit()

        result = []
        for order_1 in db.session.query(Order).all():
            result.append(order_1.to_dict())
        return jsonify(result), 200


@app.route('/orders/<int:pk>', methods=['GET'])
def read_order(pk):
    return f'{db.session.query(Order).get(pk)}'


@app.route('/offers', methods=['GET'])
def offers():
    if request.method == "GET":
        result = []
        for offer_1 in db.session.query(Offer).all():
            result.append(offer_1.to_dict())
        return jsonify(result), 200
    elif request.method == "POST":
        content = request.json
        offer_add_all = [Offer(**row) for row in content]
        db.session.add(offer_add_all)
        db.session.commit()

        result = []
        for offer_1 in db.session.query(Offer).all():
            result.append(offer_1.to_dict())
        return jsonify(result), 200


@app.route('/offers/<int:pk>', methods=['GET'])
def read_offer(pk):
    return f'{db.session.query(Offer).get(pk).order_1}\n{db.session.query(Offer).get(pk).user}'


if __name__ == "__main__":
    app.run(debug=True)
