from .user import user_bp
from .product import product_bp
from .company import company_bp
from .order import order_bp
from .place import place_bp


# Blueprintをリストとしてまとめる
blueprints = [
  user_bp,
  product_bp,
  company_bp,
  order_bp,
  place_bp
]
