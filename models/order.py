from peewee import Model, ForeignKeyField, DateTimeField
from .db import db
from .user import User
from .place import Place

class Order(Model):
    user = ForeignKeyField(User, backref='orders')
    place = ForeignKeyField(Place, backref='orders')
    order_date = DateTimeField()

    class Meta:
        database = db
