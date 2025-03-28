from flask import Flask, jsonify, request, send_file

import os

from datetime import datetime
from flask import Flask, request, render_template, url_for, send_file, redirect
from flask_cors import CORS, cross_origin
from flask import send_from_directory
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
from flask_login import LoginManager
from flask_login import login_user
from flask_login import login_required, current_user, logout_user
from flask_login import UserMixin
import os

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import IntegerField, StringField, SubmitField, FileField
from wtforms.validators import DataRequired

import threading
import os
import requests
import imaplib

import random
import json

from api.bckend_api import create_mailbox, delete_mailbox, status_server, check_mailbox, upadate_smtp

class Acc(UserMixin):
    is_authenticated = False
    is_active = False
    is_anonymous = True
    name = None

    def __init__(self, username) -> None:
        if username != None:
            self.is_authenticated = True
            self.is_active = True
            self.is_anonymous = False
            self.name = username
    
    def get_id(self):
        return str(self.name)
    
class MyForm(FlaskForm):
    recaptcha = RecaptchaField()

class MyForm2(FlaskForm):
    name = StringField('name', validators=[DataRequired()])

class MyForm3(FlaskForm):
    p = StringField('p', validators=[DataRequired()])

def check_login(username, password):
    try:
        imap = imaplib.IMAP4_SSL(host=mail_host)
        imap.login(username, password)
        return True
    except:
        return False

app = Flask(__name__)
app.url_map.strict_slashes = False
cors = CORS(app)
app.config['SECRET_KEY'] = '<SUPER_RANDOM_SECRET_KEY>'
bootstrap = Bootstrap(app)

mail_host:str = open("static/conf.txt", "r").read().split("\n")[0]

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Acc(user_id)

@app.route('/user')
# @login_required
def user():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    data, quota, used_quota, smtp_access, percent_in_use = check_mailbox(current_user.name)
    return render_template("user.html", per_used=percent_in_use, quota=quota, used_quota=used_quota, smtp_access=smtp_access)

@app.route('/unblock-smtp', methods=["POST"])
# @login_required
def change_smtp():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    switch = request.form.get("turnoffon")
    print(type(switch))
    if switch == "0":
        mode = "1"
    else:
        mode = "0"
    upadate_smtp(current_user.name, mode)
    return redirect(url_for("user"))

@app.route('/auth_login', methods=['POST'])
def login_post():
    if current_user.is_authenticated:
        return redirect(url_for("user"))
    username = request.form.get("input_username")
    password = request.form.get("password")
    remember = True if request.form.get("rem") else False
    if status:=check_login(username, password):
        user = Acc(username)
        login_user(user, remember=remember)
        return redirect(url_for("user"))
    return redirect(url_for("login", status="error"))

@app.route("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("user"))
    form = MyForm2()
    status = None
    if request.args:
        status = request.args.get("status")
    return render_template("login.html", form=form, message_alert=status)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    # return render_template("login.html", form=MyForm(), message_alert="none")
    return redirect(url_for("login"))

@app.route('/delete/<email>')
@login_required
def delete(email):
    logout_user()
    delete_mailbox(email)
    return redirect(url_for("login"))

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/images'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/robots.txt')
def robots():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'robots.txt')

@app.route('/light.png')
def logo_icon_light():
    return send_from_directory(os.path.join(app.root_path, 'static/images'),
                               'logo_icon.png', mimetype='image/png')

@app.route('/dark.png')
def logo_icon():
    return send_from_directory(os.path.join(app.root_path, 'static/images'),
                               'logo_icon.png', mimetype='image/png')

@app.route('/logo_icon.png')
def logo():
    return send_from_directory(os.path.join(app.root_path, 'static/images'),
                               'logo_icon.png', mimetype='image/png')

@app.route('/logo_.png')
def logo_icon_2():
    return send_from_directory(os.path.join(app.root_path, 'static/images'),
                               'logo_icon.png', mimetype='image/png')

@app.route("/banner/<filename>", methods=['GET'])
def load_image(filename):
    return send_from_directory(os.path.join("static", "banners"), filename, mimetype='image/png')

@app.route("/", methods=['GET', 'POST'])
def index():
    gf:list = open("static/g.txt", "r").read().split("\n")
    g:str = random.choice(random.sample(gf, len(gf)))
    array:list = []
    count:int = 0
    for _ in open("static/.domains", "r").read().split("\n"):
        if _!=None and _!="":
            try:
                count+=int(_.split(",")[1])
            except:
                pass
            array.append({"dm": _.split(",")[0], "cu": _.split(",")[1]})
    prec:int = (count/25000)*100
    style = f'style="width: {prec}%"'
    bg_class = random.choice(["bg-danger", "bg-info", "bg-warning", "bg-danger", "bg-success"])
    return render_template("index.html", g=g, filedata=array, prec=prec, count=count, bg_class=bg_class, style=style)

@app.route("/help", methods=['GET', 'POST'])
def help():
    return render_template("help.html")

@app.route("/add-domain", methods=['GET', 'POST'])
def add_domain():
    return render_template("add_domain.html")

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    return render_template("contact.html")

@app.route("/donate", methods=['GET', 'POST'])
def donate():
    return render_template("donate.html")

@app.route("/limited-domains", methods=["GET", "POST"])
def limited_domains():
    form = MyForm()
    array = []
    for _ in open("static/.domains", "r").read().split("\n"):
        if _!=None and _!="":
            array.append({"dm": _.split(",")[0], "cu": _.split(",")[1]})
    if request.form:
        d = request.form.get("d")
        p = request.form.get("p")
        username = request.form.get("username")
        password = request.form.get("password")
        domains = []
        passwords = []
        for domain in open("static/.limited_domains", "r").read().split("\n"):
            try:
                domains.append(domain.split(",")[0])
                passwords.append(domain.split(",")[1])
            except:
                continue
        for domain in range(len(domains)):
            if d == domains[domain]:
                if p == passwords[domain]:
                    message_alert:str = create_mailbox(username, password, d)
                    error_message = ""
                    if message_alert == "error":
                        error_message = "Can not create user."
                    if message_alert == "alert":
                        error_message = "User already exists!"
                    return render_template('register.html', form=form, filedata=array, message_alert=message_alert, error_message=error_message)
        return redirect(url_for("limited_domains", message_alert="Wrong password"))
    if not request.args:
        return redirect(url_for("register"))
    form = MyForm3()
    d = request.args.get("d")
    username = request.args.get("username")
    password = request.args.get("password")
    message_alert = ""
    try:
        message_alert = request.args.get("message_alert")
    except:
        pass
    return render_template("limited.html", d=d, form=form, username=username, password=password, message_alert=message_alert)

def verify_cf(response):
    secret:str = "<SUPER_SECRET_CF_KEY>"
    url:str = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
    data:dict = {"secret":secret,
        "response":response}
    res = requests.post(url, data=data)
    data = json.loads(res.text)
    if data["success"]:
        return True
    return False

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("user"))
    form = MyForm()
    array:list = []
    message_alert:str = ""
    error_message:str = ""
    for _ in open("static/.domains", "r").read().split("\n"):
        if _!=None and _!="":
            array.append({"dm": _.split(",")[0], "cu": _.split(",")[1]})
    if request.form:
        cf_res = request.form.get("cf-turnstile-response")
        if not verify_cf(cf_res):
            message_alert = "error"
            error_message = "Prove your humanity E.T."
            return render_template('register.html', form=form, filedata=array, message_alert=message_alert, error_message=error_message)
        username = request.form.get("input_username")
        password = request.form.get("password")
        domain = request.form.get("domains")
        limited_domains = open("static/.limited_domains", "r").read().split("\n")
        domains = []
        passwords = []
        for do in limited_domains:
            try:
                d = do.split(",")[0]
                p = do.split(",")[1]
            except:
                continue
            domains.append(d)
            passwords.append(p)
        if domain in domains:
            for _ in range(len(domains)):
                if domain == domains[_]:
                    # return render_template("limited.html", d=domains[_], p=passwords[_])
                    return redirect(url_for("limited_domains", d=domains[_], username=username, password=password))
        if domain != "Choose...":
            message_alert:str = create_mailbox(username, password, domain)
        if message_alert == "error":
            error_message = "Can not create user."
        if message_alert == "alert":
            error_message = "User already exists!"
        if domain == "Choose...":
            message_alert = "alert"
            error_message = "Choose right domain!"
    return render_template('register.html', form=form, filedata=array, message_alert=message_alert, error_message=error_message)

@app.route("/status")
def check_status_server():
    errors, data = status_server()
    return render_template("status.html", errors=errors, data=data)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

app.run(host="0.0.0.0", port=5050)