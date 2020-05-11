import requests
from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required

from app import db
from app import maps
from app.forms import OrderCreateForm
from app.models import Order
from helpers import is_safe_url

__doc__ = """Модуль веб-страниц для создания, редактирования и отображения заказов"""

blueprint = Blueprint(
    'orders',
    __name__,
    template_folder='templates'
)


@blueprint.route('/orders/create', methods=['POST', 'GET'])
@login_required
def create():
    """Создание заказа"""
    form = OrderCreateForm(obj=current_user)
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
    return render_template('orders_create.html', form=form)


@blueprint.route('/orders/<int:id>/change', methods=['GET', 'POST'])
@login_required
def change(id):
    """Изменение заказа"""
    pass


@blueprint.route('/orders/<int:id>/delete')
@login_required
def delete(id):
    """Удаление заказа"""
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
    """Отображение свободных заказов"""
    orders = Order.query.filter(
        Order.volunteer_id == None,
        Order.client != current_user
    ).all()
    return render_template('orders_free.html', orders=orders)


@blueprint.route('/orders/given/done', defaults={'done': True})
@blueprint.route('/orders/given', defaults={'done': False})
@login_required
def given(done):
    """Отображение заказов, отданных пользователем"""
    orders = Order.query.filter(
        Order.client == current_user,
        Order.done == done
    ).all()
    return render_template('orders_given.html', orders=orders, done=done)


@blueprint.route('/orders/<int:id>/take')
@login_required
def take(id):
    """Взятие заказа"""
    order = Order.query.get(id)
    if order.client == current_user:
        flash('Вы не можете взять собственный заказ.')
        return redirect(url_for('.free'))
    count = Order.query.filter(
        Order.volunteer == current_user,
        Order.done == False
    ).count()
    if count > 3:
        flash('Вы не можете взять больше 3 заказов.')
        return redirect(url_for('.free'))
    order.volunteer = current_user
    db.session.add(order)
    db.session.commit()
    flash('Вы приняли заказ.')
    return redirect(url_for('.taken'))


@blueprint.route('/orders/taken/done', defaults={'done': True})
@blueprint.route('/orders/taken', defaults={'done': False})
@login_required
def taken(done):
    """Отображение взятых заказов"""
    orders = Order.query.filter(
        Order.volunteer == current_user,
        Order.done == done
    ).all()
    return render_template('orders_taken.html', orders=orders, done=done)


@blueprint.route('/orders/<int:id>/about')
@login_required
def about(id):
    """Отображение подробной информации о заказе"""
    order = Order.query.get(id)
    res = maps.geocoder_api(geocode=f"Новосибирск, {order.address}")
    toponym = res["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    cs = toponym_coodrinates.split()
    address_ll = f"{cs[0]},{cs[1]}"

    search_params = {
        "ll": address_ll,
        "spn": "0.005,0.005",
        "type": "biz"
    }

    res = maps.geosearch_api(**search_params, text='супермаркет')
    organization = res["features"][0]
    point = organization["geometry"]["coordinates"]
    shop_point = f'{point[0]},{point[1]}'

    res = maps.geosearch_api(**search_params, text='аптека')
    organization = res["features"][0]
    point = organization["geometry"]["coordinates"]
    apteka_point = f'{point[0]},{point[1]}'

    points = [
        (address_ll, 'pm2rdm'),
        (shop_point, 'pm2lbm'),
        (apteka_point, 'pm2gnm')
    ]
    map_request = maps.static_api('map', pt='~'.join(f'{i[0]},{i[1]}' for i in points))
    return render_template('orders_about.html', order=order, map_file=map_request)


@blueprint.route('/orders/<int:id>/volunteer_confirm')
@login_required
def volunteer_confirm(id):
    """Подтверждение заказа от волонтёра"""
    order = Order.query.get(id)
    order.volunteer_confirm = True
    if order.client_confirm:
        order.done = True
    db.session.add(order)
    db.session.commit()
    return redirect(url_for('orders.taken'))


@blueprint.route('/orders/<int:id>/client_confirm')
@login_required
def client_confirm(id):
    """Подтверждение заказа от клиента"""
    order = Order.query.get(id)
    order.client_confirm = True
    if order.volunteer_confirm:
        order.done = True
    db.session.add(order)
    db.session.commit()
    return redirect(url_for('orders.given'))

