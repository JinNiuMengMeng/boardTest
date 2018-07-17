# -*- coding: utf-8 -*-
from flask import render_template, redirect, request, url_for, flash, session, jsonify
from app.main import auth
from app.main.forms.baseforms import LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import ctypes
from constants.errorCode import EC_GETGPI, EC_INIT, EC_SETGPO, EC_ARGS
import os
# from constants.testPygpio import pygpio

pygpio = ctypes.cdll.LoadLibrary("/home/root/libgpio.so")

selected = lambda x: 1 if x else 0


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
@admin_login_req
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
@admin_login_req
def logout():
    session.pop("admin", None)
    flash('您已退出')
    return redirect(url_for('auth.index'))


@auth.route('/change_password')
@admin_login_req
def change_password():
    return redirect(url_for('auth.index'))


@auth.route('/get/gpi/data', methods=["GET", "POST"])
@admin_login_req
def get_gpi_data():
    port_values = []
    for i in range(0, 8):
        port_values.append(pygpio.gpi_get(i))

    if -1 in port_values:
        success = False
        error_code = EC_GETGPI
        message = str(port_values.index(-1) + 1) + "端口状态获取失败."
    else:
        success = True
        error_code = 0
        message = ""
    data = {
        "gpilist": [{"name": "gpi1", "value": port_values[0]}, {"name": "gpi2", "value": port_values[1]},
                    {"name": "gpi3", "value": port_values[2]}, {"name": "gpi4", "value": port_values[3]},
                    {"name": "gpi5", "value": port_values[4]}, {"name": "gpi6", "value": port_values[5]},
                    {"name": "gpi7", "value": port_values[6]}, {"name": "gpi8", "value": port_values[7]}]
    }
    return jsonify({"success": success, "message": message, "error_code": error_code, "data": data})


@auth.route('/init', methods=["GET", "POST"])
@admin_login_req
def get_init_data():
    if pygpio.gpio_init() == 0:
        port_values = []
        for i in range(0, 8):
            port_values.append(pygpio.gpi_get(i))

        if -1 in port_values:
            success = False
            error_code = EC_GETGPI
            message = str(port_values.index(-1) + 1) + "端口状态获取失败."
        else:
            success = True
            error_code = 0
            message = ""
        data = {
            "gpilist": [{"name": "gpi1", "value": port_values[0]}, {"name": "gpi2", "value": port_values[1]},
                        {"name": "gpi3", "value": port_values[2]}, {"name": "gpi4", "value": port_values[3]},
                        {"name": "gpi5", "value": port_values[4]}, {"name": "gpi6", "value": port_values[5]},
                        {"name": "gpi7", "value": port_values[6]}, {"name": "gpi8", "value": port_values[7]}],
            "gpolist": [{"name": "gpo1", "value": "0"}, {"name": "gpo2", "value": "0"}, {"name": "gpo3", "value": "0"},
                        {"name": "gpo4", "value": "0"}, {"name": "gpo5", "value": "0"}, {"name": "gpo6", "value": "0"},
                        {"name": "gpo7", "value": "0"}, {"name": "gpo8", "value": "0"}]}
    else:
        success = False
        error_code = EC_INIT
        message = "初始化失败"
        data = ""
    return jsonify({"success": success, "message": message, "error_code": error_code, "data": data})


@auth.route('/update/gpo', methods=["GET", "POST"])
@admin_login_req
def update_gpo():
    gpoNum = request.args.get("gpoNum")
    portNum = request.args.get("portNum")
    if gpoNum != None and portNum != None:
        gpoNum = int(gpoNum)
        portNum = int(portNum[-1]) - 1
        set_gpo = pygpio.gpo_set(portNum, gpoNum)
        if set_gpo == 0 or set_gpo == 1:
            gpiNum = pygpio.gpi_get(portNum)
            if gpiNum == 0 or gpiNum == 1:
                data = {"name": portNum, "value": gpiNum}
                success = True
                error_code = 0
                message = ""
            else:
                data = ""
                success = False
                error_code = EC_GETGPI
                message = "端口状态获取失败"
        else:
            data = ""
            success = False
            error_code = EC_SETGPO
            message = "设置端口状态失败"
    else:
        success = False
        error_code = EC_ARGS
        message = "缺少参数"
        data = ""
    return jsonify({"success": success, "error_code": error_code, "message": message, "data": data})


@auth.route('/reboot', methods=["GET", "POST"])
@admin_login_req
def reboot():
    session.pop("admin", None)
    os.system('reboot')
    return redirect(url_for('auth.index'))
