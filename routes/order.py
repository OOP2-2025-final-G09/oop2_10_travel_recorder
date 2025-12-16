from flask import Blueprint, render_template, request, redirect, url_for
from models import Order, Traveler, Place, Company
from datetime import datetime, date


# Blueprintの作成
order_bp = Blueprint('order', __name__, url_prefix='/orders')


@order_bp.route('/')
def list():
    orders = Order.select()
    return render_template('order_list.html', title='注文一覧', items=orders)


@order_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':

        traveler_id = int(request.form['traveler_id'])
        place_id = int(request.form['place_id'])
        company_id = int(request.form['company_id'])
        order_date = datetime.strptime(request.form['order_date'], "%Y-%m-%d")

        # --- ここを追加：存在チェック ---
        if not Company.get_or_none(Company.id == company_id):
            return "会社が存在しません。", 400
        if not Place.get_or_none(Place.id == place_id):
            return "目的地が存在しません。", 400
        # ----------------------------------

        Order.create(
            traveler=traveler_id,
            place=place_id,
            company=company_id,
            order_date=order_date
    )

        return redirect(url_for('order.list'))

    # ForeignKey の候補一覧
    travelers = Traveler.select()
    places = Place.select()
    companies = Company.select()

    return render_template(
        'order_add.html',
        travelers=travelers,
        places=places,
        companies=companies,
        current_date=date.today()
    )



@order_bp.route('/edit/<int:order_id>', methods=['GET', 'POST'])
def edit(order_id):
    order = Order.get_or_none(Order.id == order_id)
    if not order:
        return redirect(url_for('order.list'))

    if request.method == 'POST':
        traveler_id = int(request.form['traveler_id'])
        place_id = int(request.form['place_id'])
        company_id = int(request.form['company_id'])
        order_date = datetime.strptime(request.form['order_date'], "%Y-%m-%d")


        # --- ここを追加：存在チェック ---
        if not Company.get_or_none(Company.id == company_id):
            return "会社が存在しません。", 400
        if not Place.get_or_none(Place.id == place_id):
            return "目的地が存在しません。", 400
        # ----------------------------------

        order.traveler= traveler_id
        order.place = place_id
        order.company = company_id
        order.order_date = order_date
        order.save()

        return redirect(url_for('order.list'))


    # 外部キー用の候補一覧を渡す
    travelers = Traveler.select()
    places = Place.select()
    companies = Company.select()

    return render_template(
        'order_edit.html',
        order=order,
        travelers=travelers,
        places=places,
        companies=companies
    )