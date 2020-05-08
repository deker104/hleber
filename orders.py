from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import url_for
from flask import request
from helpers import is_safe_url
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
    db.session.query(Order).filter(Order.id == id).delete()
    db.session.commit()
    next = request.referrer
    if next is None or not is_safe_url(next):
        next = url_for('index')
    flash('Вы удалили запись.')
    return redirect(next)


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


@blueprint.route('/orders/<int:id>/take')
@login_required
def take(id):
    query = Order.query.get(id)
    if Order.query.filter(Order.volunteer == current_user, not Order.done).count() < 3:
        query.volunteer = current_user
        db.session.add(query)
        db.session.commit()
        flash('Вы приняли запрос.')
        return redirect('/orders/doing')
    else:
        flash('Вы не можете взять больше 3 заказов.')
        return redirect('/orders/free')



@blueprint.route('/orders/doing')
@login_required
def doing():
    query = Order.query.filter(Order.volunteer == current_user)
    return render_template('orders_doing.html', query=query)

