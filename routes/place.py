from flask import Blueprint, render_template, request, redirect, url_for
from models import Place

# Blueprintの作成
place_bp = Blueprint('place', __name__, url_prefix='/places')


@place_bp.route('/')
def list():
    places = Place.select()
    return render_template('place_list.html', title='目的地一覧', items=places)


@place_bp.route('/add', methods=['GET', 'POST'])
def add():

    # 選択肢
    PLACE_OPTIONS = {
        1: "沖縄",
        2: "名古屋",
        3: "北海道"
    }

    if request.method == 'POST':
        place_id = int(request.form['place_id'])

        # 既に存在するIDは追加しない（＝固定データ）
        existing = Place.get_or_none(Place.id == place_id)
        if not existing:
            Place.create(id=place_id, name=PLACE_OPTIONS[place_id])

        return redirect(url_for('place.list'))

    return render_template('place_add.html')


@place_bp.route('/edit/<int:place_id>', methods=['GET', 'POST'])
def edit(place_id):
    PLACE_OPTIONS = {
        1: "沖縄",
        2: "名古屋",
        3: "北海道"
    }

    place = Place.get_or_none(Place.id == place_id)
    if not place:
        return redirect(url_for('place.list'))

    if request.method == 'POST':
        new_place_id = int(request.form['place_id'])
        place.id = new_place_id
        place.name = PLACE_OPTIONS[new_place_id]
        place.save()
        return redirect(url_for('place.list'))

    return render_template('place_edit.html', place=place)
