from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import url_for
from flask_login import current_user
from flask_login import login_required

from forms import MakeOrder
from models import Order
from web import db

blueprint = Blueprint(
    'orders',
    __name__,
    template_folder='templates'
)


@blueprint.route('/orders/create', methods=['POST', 'GET'])
@login_required
def create():
    form = MakeOrder()
    if form.validate_on_submit():
        order = Order(
            address=form.address.data,
            phone=form.phone.data,
            client_id=current_user.id,
            text=form.text.data
        )
        db.session.add(order)
        db.session.commit()
        flash('Успешно добавлен/изменён заказ.')
        return redirect(url_for('.given'))
    form.phone.data = current_user.phone
    return render_template('orders_create.html', form=form)


@blueprint.route('/orders/<int:id>/change', methods=['GET', 'POST'])
@login_required
def change(id):
    pass


@blueprint.route('/orders/<int:id>/delete')
@login_required
def delete(id):
    return '<h1>Успех!</h1>'


@blueprint.route('/orders/free')
@login_required
def free():
    query = Order.query.filter(
        Order.volunteer_id == None,
        Order.client != current_user
    )
    return render_template('orders_free.html', query=query)


@blueprint.route('/orders/given')
@login_required
def given():
    query = current_user.orders_given
    return render_template('orders_given.html', query=query)

