from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required

from app import db
from app.forms import MakeOrder
from app.helpers import is_safe_url
from app.models import Order

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
        next = url_for('main.index')
    flash('Вы удалили запись.')
    return redirect(next)


@blueprint.route('/orders/free')
@login_required
def free():
    query = Order.query.filter(
        Order.volunteer_id == None,
        Order.client != current_user
    ).all()
    return render_template('orders_free.html', query=query)


@blueprint.route('/orders/given')
@login_required
def given():
    query = Order.query.filter(
        Order.client == current_user,
        Order.done == False
    ).all()
    return render_template('orders_given.html', query=query)


@blueprint.route('/orders/<int:id>/take')
@login_required
def take(id):
    query = Order.query.get(id)
    count = Order.query.filter(
        Order.volunteer == current_user,
        Order.done == False
    ).count()
    if count < 3:
        query.volunteer = current_user
        db.session.add(query)
        db.session.commit()
        flash('Вы приняли заказ.')
        return redirect(url_for('.taken'))
    else:
        flash('Вы не можете взять больше 3 заказов.')
        return redirect(url_for('.free'))


@blueprint.route('/orders/taken')
@login_required
def taken():
    query = Order.query.filter(
        Order.volunteer == current_user,
        Order.done == False
    ).all()
    return render_template('orders_taken.html', query=query)


@blueprint.route('/orders/<int:id>/about')
@login_required
def about(id):
    order = Order.query.filter(Order.id == id).first()
    return render_template('orders_about.html', order=order)


@blueprint.route('/orders/<int:id>/confirm')
@login_required
def confirm(id):
    order = Order.query.get(id)
    order.volunteer_confirm = True
    db.session.add(order)
    db.session.commit()
    return redirect(url_for('orders.taken'))
