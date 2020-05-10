from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required

from app import db
from app.forms import OrderCreateForm
from helpers import is_safe_url
from app.models import Order
import requests

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
    return render_template('orders_taken.html', orders=orders)


@blueprint.route('/orders/<int:id>/about')
@login_required
def about(id):
    """Отображение подробной информации о заказе"""
    order = Order.query.filter(Order.id == id).first()
    geo_request = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&" +\
                  f"geocode={'Новосибирск, ' + order.address}&format=json"
    response = requests.get(geo_request)
    map_request = None
    if response:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"]
        cs = toponym_coodrinates.split()
        search_api_server = "https://search-maps.yandex.ru/v1/"
        api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

        address_ll = f"{cs[0]},{cs[1]}"

        search_params = {
            "apikey": api_key,
            "text": "супермаркет",
            "lang": "ru_RU",
            "ll": address_ll,
            "type": "biz"
        }

        response = requests.get(search_api_server, params=search_params)
        json_response = response.json()
        organization = json_response["features"][0]
        point = organization["geometry"]["coordinates"]
        org_point = "{0},{1}".format(point[0], point[1])
        print(org_point)
        map_request = f"""http://static-maps.yandex.ru/1.x/?pt={cs[0]},{cs[1]},pm2rdm~{org_point},pm2lbm&l=map"""
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

