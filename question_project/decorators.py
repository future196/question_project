from flask import session, redirect, url_for, render_template
from functools import wraps

# wraper 是防止丢失原来的函数属性，可以多次调用

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("user_id"):
            return func(*args, **kwargs)
        else:
            return render_template("login_required.html")
    return wrapper
