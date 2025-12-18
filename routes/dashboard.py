# ダッシュボード用のデータ集計API
# 担当A: このファイルを実装

from flask import Blueprint, jsonify
from models import Order, Traveler, Place

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api')

@dashboard_bp.route('/age_distribution')
def age_distribution():
    age_dist = {}

    for traveler in Traveler.select():
        if traveler.age is None:
            continue

        decade = (traveler.age // 10) * 10
        age_dist[decade] = age_dist.get(decade, 0) + 1

    # キーでソートしてから jsonify
    sorted_dist = dict(sorted(age_dist.items()))

    return jsonify(sorted_dist)

@dashboard_bp.route('/popular_places')
def popular_places():
    place_count = {}

    for order in Order.select():
        place = order.place
        if place is None:
            continue

        name = place.name
        place_count[name] = place_count.get(name, 0) + 1

    place_dist = dict(sorted(place_count.items()))
    return jsonify(place_dist)

@dashboard_bp.route('/busy_dates')
def busy_dates():
    date_count = {}

    for order in Order.select():
        if order.order_date is None:
            continue

        date_str = order.order_date.strftime('%Y/%m/%d')

        date_count[date_str] = date_count.get(date_str, 0) + 1

    sorted_dates = dict(
        sorted(
            date_count.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
    )

    return jsonify(sorted_dates)
