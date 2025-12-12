from flask import Blueprint, render_template, request, redirect, url_for
from models import Order, User, Place, Company
from datetime import datetime, date

# Blueprintの作成
order_bp = Blueprint('order', __name__, url_prefix='/orders')


@order_bp.route('/')
def list():
    orders = Order.select()
    return render_template('order_list.html', title='旅行記録一覧', items=orders)


@order_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # フォームから入力値を取得
        user_name = request.form['user_name'].strip()
        user_age = int(request.form['user_age'].strip())
        place_name = request.form['place_name'].strip()
        company_name = request.form['company_name'].strip()
        order_date = datetime.strptime(request.form['order_date'], "%Y-%m-%d")

        # ユーザー取得 or 作成
        user, created = User.get_or_create(
            name=user_name,
            defaults={'age': user_age}
        )
        if not created:
            user.age = user_age
            user.save()

        # Place取得 or 作成
        place, _ = Place.get_or_create(name=place_name)

        # Company取得 or 作成
        company, _ = Company.get_or_create(name=company_name)

        # Order作成
        Order.create(user=user, place=place, company=company, order_date=order_date)

        return redirect(url_for('order.list'))

    # GET時は今日の日付を初期値として渡す
    return render_template('order_add.html', current_date=date.today())


@order_bp.route('/edit/<int:order_id>', methods=['GET', 'POST'])
def edit(order_id):
    order = Order.get_or_none(Order.id == order_id)
    if not order:
        return redirect(url_for('order.list'))

    if request.method == 'POST':
        # フォームから入力値を取得
        user_name = request.form['user_name'].strip()
        user_age = int(request.form['user_age'].strip())
        place_name = request.form['place_name'].strip()
        company_name = request.form['company_name'].strip()
        order_date_str = request.form['order_date'].strip()

        # ForeignKey用オブジェクト取得 or 作成
        user, created = User.get_or_create(
            name=user_name,
            defaults={'age': user_age}
        )
        if not created:
            user.age = user_age
            user.save()

        place, _ = Place.get_or_create(name=place_name)
        company, _ = Company.get_or_create(name=company_name)

        # Orderを更新
        order.user = user
        order.place = place
        order.company = company
        order.order_date = datetime.strptime(order_date_str, "%Y-%m-%d")
        order.save()

        return redirect(url_for('order.list'))

    # GET時はフォーム表示
    return render_template(
        'order_edit.html',
        order=order
    )

