from .user import user_bp
from .place import place_bp
from .order import order_bp

# Blueprintをリストとしてまとめる
blueprints = [
  user_bp,
  place_bp,
  order_bp
]
