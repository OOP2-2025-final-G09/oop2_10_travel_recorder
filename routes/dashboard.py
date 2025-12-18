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
    """
    利用が多かった日: 予約が集中している日付トップ10を返す
    TODO: Orderテーブルから日付別の集計を実装
    例: [{'date': '2025/1/4', 'count': 2}, {'date': '2025/1/15', 'count': 1}]
    """
    # TODO: 実装する
    return jsonify([])
