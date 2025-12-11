from peewee import Model, ForeignKeyField, DateTimeField
from .db import db
from .user import Traveler
from .product import Product

class Order(Model):
    traveler = ForeignKeyField(Traveler, backref='orders')
    product = ForeignKeyField(Product, backref='orders')
    order_date = DateTimeField()

    class Meta:
        database = db
