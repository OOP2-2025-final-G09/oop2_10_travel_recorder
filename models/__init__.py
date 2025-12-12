from peewee import SqliteDatabase
from .db import db
from .user import User

from .place import Place
from .product import Product
from .company import Company
from .order import Order
from .place import Place

# モデルのリストを定義しておくと、後でまとめて登録しやすくなります
MODELS = [
    User,
    Place,
    Product,
    Company,
    Place,
    Order,
]

# データベースの初期化関数
def initialize_database():
    db.connect()
    db.create_tables(MODELS, safe=True)
    db.close()