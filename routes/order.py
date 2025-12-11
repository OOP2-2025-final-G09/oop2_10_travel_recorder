from flask import Blueprint, render_template, request, redirect, url_for
from models import Order, User, Place
from datetime import datetime

# Blueprintの作成
order_bp = Blueprint('order', __name__, url_prefix='/orders')


@order_bp.route('/')
def list():
    orders = Order.select()
    return render_template('order_list.html', title='注文一覧', items=orders)


@order_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        user_id = request.form['user_id']
        place_id = request.form['place_id']
        order_date = datetime.now()
        Order.create(user=user_id, place=place_id, order_date=order_date)
        return redirect(url_for('order.list'))
    
    users = User.select()
    places = Place.select()
    return render_template('order_add.html', users=users, places=places)


@order_bp.route('/edit/<int:order_id>', methods=['GET', 'POST'])
def edit(order_id):
    order = Order.get_or_none(Order.id == order_id)
    if not order:
        return redirect(url_for('order.list'))

    if request.method == 'POST':
        order.user = request.form['user_id']
        order.place = request.form['place_id']
        order.save()
        return redirect(url_for('order.list'))

    users = User.select()
    places = Place.select()
    return render_template('order_edit.html', order=order, users=users, places=places)
