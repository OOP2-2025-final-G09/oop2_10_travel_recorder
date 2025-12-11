from flask import Blueprint, render_template, request, redirect, url_for
from models import Company

# Blueprintの作成
company_bp = Blueprint('company', __name__, url_prefix='/companys')


@company_bp.route('/')
def list():
    companys = Company.select()
    return render_template('company_list.html', title='会社一覧', items=companys)


@company_bp.route('/add', methods=['GET', 'POST'])
def add():
    
    # POSTで送られてきたデータは登録
    if request.method == 'POST':
        name = request.form['name']
        #price = request.form['price']
        #Company.create(name=name, price=price)
        Company.create(name=name)
        return redirect(url_for('company.list'))
    
    return render_template('company_add.html')


@company_bp.route('/edit/<int:company_id>', methods=['GET', 'POST'])
def edit(company_id):
    company = Company.get_or_none(Company.id == company_id)
    if not company:
        return redirect(url_for('company.list'))

    if request.method == 'POST':
        company.name = request.form['name']
        #company.price = request.form['price']
        company.save()
        return redirect(url_for('company.list'))

    return render_template('company_edit.html', company=company)