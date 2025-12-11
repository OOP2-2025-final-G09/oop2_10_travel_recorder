from peewee import Model, CharField, DecimalField
from .db import db

class Company(Model):
    name = CharField()

    class Meta:
        database = db