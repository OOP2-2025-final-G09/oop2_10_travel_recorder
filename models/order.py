from peewee import Model, ForeignKeyField, DateTimeField
from .db import db
from .user import User
from .place import Place
from .company import Company  # Companyモデルをインポート

class Order(Model):
    user = ForeignKeyField(User, backref='orders')
    place = ForeignKeyField(Place, backref='orders')
    company = ForeignKeyField(Company, backref='orders')  # 追加
    order_date = DateTimeField()

    class Meta:
        database = db
