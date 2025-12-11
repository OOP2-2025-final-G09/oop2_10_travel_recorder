from flask import Blueprint, render_template, request, redirect, url_for
from models import Order, Traveler, Product
from datetime import datetime

# Blueprintの作成
order_bp = Blueprint('order', __name__, url_prefix='/orders')


@order_bp.route('/')
def list():
    orders = Order.select()
    return render_template('order_list.html', title='旅行記録一覧', items=orders)


@order_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        traveler_id = request.form['traveler_id']
        product_id = request.form['product_id']
        order_date = datetime.now()
        Order.create(traveler=traveler_id, product=product_id, order_date=order_date)
        return redirect(url_for('order.list'))
    
    travelers = Traveler.select()
    products = Product.select()
    return render_template('order_add.html', travelers=travelers, products=products)


@order_bp.route('/edit/<int:order_id>', methods=['GET', 'POST'])
def edit(order_id):
    order = Order.get_or_none(Order.id == order_id)
    if not order:
        return redirect(url_for('order.list'))

    if request.method == 'POST':
        order.traveler = request.form['traveler_id']
        order.product = request.form['product_id']

        date_str = request.form['order_date']
        order.order_date = datetime.strptime(date_str, "%Y-%m-%d")

        order.save()
        return redirect(url_for('order.list'))

    travelers = Traveler.select()
    products = Product.select()
    return render_template('order_edit.html', order=order, travelers=travelers, products=products)
