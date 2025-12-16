from peewee import Model, CharField, DecimalField
from .db import db

class Place(Model):
    name = CharField()
    # price = DecimalField()

    class Meta:
        database = db