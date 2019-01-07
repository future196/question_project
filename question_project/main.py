from flask import Flask, render_template, request, redirect, url_for, session, g
import config
from ext import db
from model import User,Question,Answer
from decorators import login_required
from sqlalchemy import or_
import os
import time

ALLOWED_EXTENSIONS = set(['txt','pdf','png','jpg','jpeg','gif']) # 头像允许格式


app = Flask(__name__)
app.config.from_object(config)
app.config['SECRET_KEY'] = '123456'
db.init_app(app)

# with app.app_context():
#     db.create_all()

@app.route("/")
def main():
    content = {
        'questions': Question.query.order_by("-create_time")
    }
    time.sleep(5)
    return render_template("home_page.html", **content)


@app.route("/personal/")
def personnal():
    return render_template("personal.html")


# 检测头像格式是否被允许
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@app.route('/send/')
def send():
    return render_template("release_mission.html")

@app.route("/test1/",methods=['GET','POST'])
def test():
    # if request.method == "POST":

    obj = request.form.get("title")
    print(type(obj))
        # return "efrjv"
    return "sferfg"


@app.route("/change_data/", methods=['GET', 'POST'])
def change_data():
    if request.method == "POST":
        icon = request.files["icon"]
        if icon and allowed_file(icon.filename):
            file_mode = icon.filename.split(".")[1]
            user_id = session["user_id"]
            filename = str(user_id) + "." + file_mode
            icon.save(os.path.join(os.getcwd()+"\static\icon", filename))
            icon_path = "icon/"+filename
            user = User.query.filter(User.id == user_id).first()
            user.icon = icon_path
            db.session.commit()
        return redirect(url_for("main"))
    else:
        return render_template("change_data.html")


@app.route("/search/")
def search():
    q = request.args.get("q")
    questions = Question.query.filter(or_(Question.title.contains(q),
                                          Question.detail.contains(q))).order_by("-create_time")
    return render_template("home_page.html", questions=questions)


@app.route("/detail/<question_id>/")
def detail(question_id):
    content = {}
    content['question'] = Question.query.filter(Question.id == question_id).first()
    content['answers'] = Answer.query.filter(Answer.question_id == question_id).order_by("-answer_time").all()
    content['answers_num'] = len(content['answers'])
    return render_template("detail.html", **content)


@app.route("/detail/answer/", methods=['GET', 'POST'])
@login_required
def answer():
    content = request.form.get("content")
    question_id = request.form.get("question_id")
    user_id = session["user_id"]
    answer = Answer(content=content, question_id=question_id, author_id=user_id)
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for("detail", question_id=question_id))



@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        password = request.form.get("password")
        telephone = request.form.get("telephone")
        user = User.query.filter(User.telephone == telephone).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for("main"))
        else:
            return render_template("login_error.html")



@app.route("/login_up/", methods=["GET", "POST"])
def login_up():
    if request.method == "GET":
        return render_template("login_up.html")
    else:
        telephone = request.form.get("telephone")
        username = request.form.get("username")
        password = request.form.get("password")
        repick_password = request.form.get("repick_password")
        icon_default = "icon/default.png"
        isuser = User.query.filter(User.telephone == telephone).first()
        if isuser:
            return "此手机号码已注册!"
        else:
            if password == repick_password:
                user = User(telephone=telephone, username=username, password=password, icon=icon_default)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for("login"))
            else:
                return "两次输入的密码不一致!"

@app.route("/logout/")
def logout():
    session.pop("user_id")
    # del session['user_id']    # 同上
    # session.clear()       # 同上
    return redirect(url_for("login"))



@app.route("/question/", methods = ['GET','POST'])
@login_required
def question():
    if request.method == "GET":
        return render_template("question.html")
    else:
        title = request.form.get("title")
        detail = request.form.get("detail")
        author_id = session.get("user_id")
        # author_id = Question.query.filter(User.id == user_id).first()
        question = Question(title=title, detail=detail, author_id=author_id)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for("main"))


@app.before_request
def my_before_request():
    user_id = session.get("user_id")
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            g.user = user


# 上下文处理器，可提供给全局使用，可在检测全局登录状态使用
@app.context_processor
def my_text_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {"user": user}
    else:
        return {}



if __name__ == "__main__":
    app.run()