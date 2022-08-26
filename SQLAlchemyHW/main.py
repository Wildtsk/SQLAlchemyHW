from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Column, Integer, String, Text

from utils import get_users_all, get_orders_all, get_offers_all

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

# print(order)
# print(order.customer)
# print(order.executor)

# print(db.session.query(Offer).get(1).db.session.query(Order).get(1))
# print(offer.user)
# print(user)


@app.route('/users', methods=['GET'])
def read_users():
    return f'{db.session.query(User).all()}'


@app.route('/users/<int:pk>', methods=['GET'])
def read_user(pk):
    return f'{db.session.query(User).get(pk)}'


@app.route('/orders', methods=['GET'])
def read_orders():
    return f'{db.session.query(Order).all()}'


@app.route('/orders/<int:pk>', methods=['GET'])
def read_order(pk):
    return f'{db.session.query(Order).get(pk)}'


@app.route('/offers', methods=['GET'])
def read_offers():
    return f'{db.session.query(Order).all()}\n{db.session.query(User).all()}'


@app.route('/offers/<int:pk>', methods=['GET'])
def read_offer(pk):
    return f'{db.session.query(Offer).get(pk).order_1}\n{db.session.query(Offer).get(pk).user}'


@app.route('/users', methods=['POST'])
def post_user():
    content = request.form.get('content')
    user_add = [User(**row) for row in content]
    db.session.add(user_add)
    db.session.commit()
    return "Данные успешно сохранены"


# @app.route('/users/<int:pk>', methods=['PUT'])
# def put_user(pk):
#     content = request.form.get('content')
#     user_add = [User(**row) for row in content]
#     db.session.add(user_add)
#     db.session.commit()
#     return "Данные успешно сохранены"


if __name__ == "__main__":
    app.run(debug=True)