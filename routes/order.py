from flask import Blueprint, render_template, request, redirect, url_for
from models import Order, Traveler, Place, Company
from datetime import datetime, date


# Blueprintの作成
order_bp = Blueprint('order', __name__, url_prefix='/orders')


@order_bp.route('/')
def list():
    orders = Order.select()
    return render_template('order_list.html', title='注文一覧', items=orders)


from flask import request, redirect, url_for, render_template
from models import Order

@order_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        traveler_id = int(request.form['traveler_id'])
        company_id = int(request.form['company_id'])
        place_id = int(request.form['place_id'])
        order_date = request.form['order_date']

        exists = Order.select().where(
            (Order.traveler == traveler_id) &
            (Order.company == company_id) &
            (Order.place == place_id) &
            (Order.order_date == order_date)
        ).exists()

        if exists:
            return render_template(
                'order_add.html',
                error='同じユーザー・会社・目的地・日付の旅行記録は既に登録されています。',
                travelers=Traveler.select(),
                companies=Company.select(),
                places=Place.select(),
                current_date=order_date
            )

        Order.create(
            traveler=traveler_id,
            company=company_id,
            place=place_id,
            order_date=order_date
        )

        return redirect(url_for('order.list'))

    return render_template(
        'order_add.html',
        travelers=Traveler.select(),
        companies=Company.select(),
        places=Place.select(),
        current_date=date.today().isoformat()
    )


@order_bp.route('/edit/<int:order_id>', methods=['GET', 'POST'])
def edit(order_id):
    order = Order.get_or_none(Order.id == order_id)
    if not order:
        return redirect(url_for('order.list'))

    if request.method == 'POST':
        traveler_id = int(request.form['traveler_id'])
        company_id = int(request.form['company_id'])
        place_id = int(request.form['place_id'])
        order_date = request.form['order_date']

        exists = Order.select().where(
            (Order.id != order_id) &  
            (Order.traveler == traveler_id) &
            (Order.company == company_id) &
            (Order.place == place_id) &
            (Order.order_date == order_date)
        ).exists()

        if exists:
            return render_template(
                'order_edit.html',
                error='同じユーザー・会社・目的地・日付の旅行記録は既に存在します。',
                order=order,
                travelers=Traveler.select(),
                companies=Company.select(),
                places=Place.select()
            )

        order.traveler = traveler_id
        order.company = company_id
        order.place = place_id
        order.order_date = order_date
        order.save()

        return redirect(url_for('order.list'))

    return render_template(
        'order_edit.html',
        order=order,
        travelers=Traveler.select(),
        companies=Company.select(),
        places=Place.select()
    )
