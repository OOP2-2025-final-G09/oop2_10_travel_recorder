from flask import Blueprint, render_template, request, redirect, url_for
from models import Company

# Blueprintの作成
company_bp = Blueprint('company', __name__, url_prefix='/companys')

# 会社の固定選択肢
COMPANY_OPTIONS = {
    1: "JAL",
    2: "ANA",
    3: "Peach"
}


@company_bp.route('/')
def list():
    companys = Company.select()
    return render_template('company_list.html', title='会社一覧', items=companys)


@company_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        company_id = int(request.form['company_id'])

        # 既に存在しない場合だけ作成（初期データ前提）
        existing = Company.get_or_none(Company.id == company_id)
        if not existing:
            Company.create(id=company_id, name=COMPANY_OPTIONS[company_id])

        return redirect(url_for('company.list'))

    return render_template('company_add.html')


@company_bp.route('/edit/<int:company_id>', methods=['GET', 'POST'])
def edit(company_id):
    company = Company.get_or_none(Company.id == company_id)
    if not company:
        return redirect(url_for('company.list'))

    if request.method == 'POST':
        new_id = int(request.form['company_id'])

        # ID と 名前を更新
        company.id = new_id
        company.name = COMPANY_OPTIONS[new_id]
        company.save()

        return redirect(url_for('company.list'))

    return render_template('company_edit.html', company=company)
