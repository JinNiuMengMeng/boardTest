# -*- coding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, TextField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError


class LoginForm(FlaskForm):
    account = StringField(label="账号", validators=[DataRequired("请输入账号!")],
                          render_kw={"class": "layui-input", "placeholder": "请输入用户名！", "required": "required",
                                     "lay-verify": "required"})
    pwd = PasswordField(label="密码", validators=[DataRequired("请输入密码!")],
                        render_kw={"class": "layui-input", "placeholder": "请输入密码！", "required": "required",
                                   "lay-verify": "required"})
    submit = SubmitField(label="登录", render_kw={"class": "layui-btn btn-login"})

    def validate_account(self, field):  # 自定义验证器, 规则是"validate_字段名"
        pass

