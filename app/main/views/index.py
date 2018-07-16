# -*- coding: utf-8 -*-
from flask import render_template, redirect, request, url_for, flash, session, jsonify
from app.main import auth
from app.main.forms.baseforms import LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import ctypes

selected = lambda x: 1 if x else 0


# pygpio = ctypes.cdll.LoadLibrary("/home/ubuntu/Documents/libgpio.so")
pygpio = ctypes.cdll.LoadLibrary("/home/root/libgpio.so")


def admin_login_req(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("auth.login", next=request.url))
        return func(*args, **kwargs)

    return decorated_function


@auth.before_app_request
def before_request():
    print("before_app_request")


@auth.route('/', methods=["GET", "POST"])
# @admin_login_req
def index():
    return render_template("index.html")


@auth.route('/login', methods=["GET", "POST"])
def login():
    session.pop("admin", None)
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        if form.userName.data == "root" and check_password_hash(generate_password_hash(form.password.data), "root"):
            flash("登录成功")
            session["admin"] = form.userName.data
            return redirect(request.args.get("next") or url_for("auth.index"))
        else:
            flash("无效的用户名或密码")
    return render_template("login.html", form=form)


@auth.route('/logout')
# @admin_login_req
def logout():
    session.pop("admin", None)
    flash('您已退出')
    return redirect(url_for('auth.index'))


@auth.route('/change_password')
# @admin_login_req
def change_password():
    return redirect(url_for('auth.index'))


@auth.route('/get/gpi/data', methods=["GET", "POST"])
# @admin_login_req
def get_gpi_data():
    port_values = []
    for i in range(0, 8):
        value = pygpio.gpi_get(i)
        if value == 0 or value == 1:
            port_values.append(str(value))
        else:
            pass

    result = {
        "gpilist": [{"name": "gpi1", "value": port_values[0]}, {"name": "gpi2", "value": port_values[1]},
                    {"name": "gpi3", "value": port_values[2]},
                    {"name": "gpi4", "value": port_values[3]}, {"name": "gpi5", "value": port_values[4]},
                    {"name": "gpi6", "value": port_values[5]},
                    {"name": "gpi7", "value": port_values[6]}, {"name": "gpi8", "value": port_values[7]}]}
    # result = {
    #     "gpilist": [{"name": "gpi1", "value": "0"}, {"name": "gpi2", "value": "1"}, {"name": "gpi3", "value": "1"},
    #                 {"name": "gpi4", "value": "1"}, {"name": "gpi5", "value": "0"}, {"name": "gpi6", "value": "0"},
    #                 {"name": "gpi7", "value": "1"}, {"name": "gpi8", "value": "0"}]}

    return jsonify(result)


@auth.route('/get/init/data', methods=["GET", "POST"])
# @admin_login_req
def get_init_data():
    if pygpio.gpio_init() == 0:
        port_values = []
        for i in range(0, 8):
            value = pygpio.gpi_get(i)
            if value == 0 or value == 1:
                port_values.append(str(value))
            else:
                pass
    result = {
        "gpilist": [{"name": "gpi1", "value": port_values[0]}, {"name": "gpi2", "value": port_values[1]},
                    {"name": "gpi3", "value": port_values[2]},
                    {"name": "gpi4", "value": port_values[3]}, {"name": "gpi5", "value": port_values[4]},
                    {"name": "gpi6", "value": port_values[5]},
                    {"name": "gpi7", "value": port_values[6]}, {"name": "gpi8", "value": port_values[7]}],
        "gpolist": [{"name": "gpo1", "value": "0"}, {"name": "gpo2", "value": "0"}, {"name": "gpo3", "value": "0"},
                    {"name": "gpo4", "value": "0"}, {"name": "gpo5", "value": "0"}, {"name": "gpo6", "value": "0"},
                    {"name": "gpo7", "value": "0"}, {"name": "gpo8", "value": "0"}]}
    # result = {
    #     "gpilist": [{"name": "gpi1", "value": "1"}, {"name": "gpi2", "value": "0"}, {"name": "gpi3", "value": "1"},
    #                 {"name": "gpi4", "value": "0"}, {"name": "gpi5", "value": "1"}, {"name": "gpi6", "value": "0"},
    #                 {"name": "gpi7", "value": "1"}, {"name": "gpi8", "value": "0"}],
    #     "gpolist": [{"name": "gpo1", "value": "1"}, {"name": "gpo2", "value": "0"}, {"name": "gpo3", "value": "1"},
    #                 {"name": "gpo4", "value": "0"}, {"name": "gpo5", "value": "1"}, {"name": "gpo6", "value": "0"},
    #                 {"name": "gpo7", "value": "1"}, {"name": "gpo8", "value": "0"}]}

    return jsonify(result)


@auth.route('/update/gpo', methods=["GET", "POST"])
# @admin_login_req
def update_gpo():
    # set_gpo = pygpio.gpo_set(1, 1)
    result = {"name": "gpo1", "value": "1"}
    return jsonify(result)
