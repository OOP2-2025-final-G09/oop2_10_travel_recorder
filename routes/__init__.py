from .user import traveler_bp
from .product import product_bp
from .company import company_bp
from .order import order_bp

# Blueprintをリストとしてまとめる
blueprints = [
  traveler_bp,
  product_bp,
  company_bp,
  order_bp
]
