# ダッシュボード用のデータ集計API
# 担当A: このファイルを実装

from flask import Blueprint, jsonify
from models import Order, Traveler, Place

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api')

@dashboard_bp.route('/age_distribution')
def age_distribution():
    """
    利用年齢層: ユーザーの年齢分布を返す
    TODO: Travelerテーブルから年齢別の集計を実装
    例: {'20代': 2, '30代': 1}
    """
    # TODO: 実装する
    return jsonify({})


@dashboard_bp.route('/popular_places')
def popular_places():
    """
    人気の旅行先: 予約数が多い目的地を返す
    TODO: Orderテーブルから目的地別の集計を実装
    例: {'沖縄': 67, '北海道': 33}
    """
    # TODO: 実装する
    return jsonify({})


@dashboard_bp.route('/busy_dates')
def busy_dates():
    """
    利用が多かった日: 予約が集中している日付トップ10を返す
    TODO: Orderテーブルから日付別の集計を実装
    例: [{'date': '2025/1/4', 'count': 2}, {'date': '2025/1/15', 'count': 1}]
    """
    # TODO: 実装する
    return jsonify([])
