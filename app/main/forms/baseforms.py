# -*- coding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, TextField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError


class LoginForm(FlaskForm):
    userName = StringField(label="账号", validators=[DataRequired("请输入账号!")],
                          render_kw={"class": "layui-input", "placeholder": "请输入用户名！", "required": "required",
                                     "lay-verify": "required"})
    password = PasswordField(label="密码", validators=[DataRequired("请输入密码!")],
                        render_kw={"class": "layui-input", "placeholder": "请输入密码！", "required": "required",
                                   "lay-verify": "required"})
    # submit = SubmitField(label="登录", render_kw={"class": "layui-btn btn-login", "type": "button"})
    submit = SubmitField(label="登录", render_kw={"class": "btn btn-primary btn-block btn-flat"})

    # def validate_userName(self, field):  # 自定义验证器, 规则是"validate_字段名"
    #     print("验证userName------")
    #     print(field)
    #     pass
    #
    # def validate_password(self, field):
    #     print("验证password------")
    #     print(field)
    #     pass
