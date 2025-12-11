from flask import Blueprint, render_template, request, redirect, url_for
from models import Traveler

# Blueprintの作成
traveler_bp = Blueprint('traveler', __name__, url_prefix='/travelers')


@traveler_bp.route('/')
def list():
    
    # データ取得
    travelers = Traveler.select()

    return render_template('traveler_list.html', title='ユーザー一覧', items=travelers)


@traveler_bp.route('/add', methods=['GET', 'POST'])
def add():
    
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        Traveler.create(name=name, age=age)
        return redirect(url_for('traveler.list'))
    
    return render_template('traveler_add.html')


@traveler_bp.route('/edit/<int:traveler_id>', methods=['GET', 'POST'])
def edit(traveler_id):
    traveler = Traveler.get_or_none(Traveler.id == traveler_id)
    if not traveler:
        return redirect(url_for('traveler.list'))

    if request.method == 'POST':
        traveler.name = request.form['name']
        traveler.age = request.form['age']
        traveler.save()
        return redirect(url_for('traveler.list'))

    return render_template('traveler_edit.html', traveler=traveler)