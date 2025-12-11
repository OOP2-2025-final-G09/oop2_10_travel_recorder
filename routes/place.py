from flask import Blueprint, render_template, request, redirect, url_for
from models import Place

# Blueprintの作成
place_bp = Blueprint('place', __name__, url_prefix='/places')


@place_bp.route('/')
def list():
    places = Place.select()
    return render_template('place_list.html', title='製品一覧', items=places)


@place_bp.route('/add', methods=['GET', 'POST'])
def add():
    
    # POSTで送られてきたデータは登録
    if request.method == 'POST':
        name = request.form['name']
        # price = request.form['price']
        # Place.create(name=name, price=price)
        Place.create(name=name)
        return redirect(url_for('place.list'))
    
    return render_template('place_add.html')


@place_bp.route('/edit/<int:place_id>', methods=['GET', 'POST'])
def edit(place_id):
    place = Place.get_or_none(Place.id == place_id)
    if not place:
        return redirect(url_for('place.list'))

    if request.method == 'POST':
        place.name = request.form['name']
        # place.price = request.form['price']
        place.save()
        return redirect(url_for('place.list'))

    return render_template('place_edit.html', place=place)