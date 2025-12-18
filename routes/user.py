from flask import Blueprint, render_template, request, redirect, url_for, abort
from models import Traveler

# Blueprintの作成
traveler_bp = Blueprint('traveler', __name__, url_prefix='/travelers')


@traveler_bp.route('/')
def list():
    travelers = Traveler.select()
    return render_template('user_list.html', title='ユーザー一覧', items=travelers)


@traveler_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        age = int(request.form.get('age', -1))

        # 🔽 年齢チェック
        if not (0 <= age <= 100):
            abort(400, '年齢は0〜100の範囲で入力してください')

        Traveler.create(name=name, age=age)
        return redirect(url_for('traveler.list'))

    return render_template('user_add.html')


@traveler_bp.route('/edit/<int:traveler_id>', methods=['GET', 'POST'])
def edit(traveler_id):
    traveler = Traveler.get_or_none(Traveler.id == traveler_id)
    if not traveler:
        return redirect(url_for('traveler.list'))

    if request.method == 'POST':
        traveler.name = request.form['name']
        age = int(request.form.get('age', -1))

        # 🔽 年齢チェック
        if not (0 <= age <= 100):
            abort(400, '年齢は0〜100の範囲で入力してください')

        traveler.age = age
        traveler.save()
        return redirect(url_for('traveler.list'))

    return render_template('user_edit.html', traveler=traveler)
