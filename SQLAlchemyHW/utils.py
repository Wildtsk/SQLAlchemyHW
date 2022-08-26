from flask import json, jsonify


def get_users_all() -> list[dict]:
    """Возвращает всех людей"""
    with open("users.json", "r", encoding="utf-8") as file:
        return json.load(file)


def get_orders_all() -> list[dict]:
    """Возвращает все заказы"""
    with open("orders.json", "r", encoding="utf-8") as file:
        return json.load(file)


def get_offers_all() -> list[dict]:
    """Возвращает все предложения"""
    with open("offers.json", "r", encoding="utf-8") as file:
        return json.load(file)
