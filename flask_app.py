
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, LoginManager, UserMixin, logout_user, login_required, current_user
from flask_migrate import Migrate
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

app = Flask(__name__)
app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="yashmayya",
    password="adsfdgfhgj",
    hostname="yashmayya.mysql.pythonanywhere-services.com",
    databasename="yashmayya$comments",
)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.secret_key = "dhfadfcnkahsjgnfkashjxskahscnjdf"
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username

all_users = {"admin":User("admin", generate_password_hash("secret")), "yash":User("admin", generate_password_hash("adsfdgfhgj"))}

@login_manager.user_loader
def load_user(user_id):
    return all_users.get(user_id)

class Comment(db.Model):

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))
    posted = db.Column(db.DateTime, default=datetime.now)

@app.route('/', methods=['GET','POST'])
def index():

    if request.method == 'GET':
        return render_template("main_page.html", comments=Comment.query.all())

    else:
        if not current_user.is_authenticated:
            return redirect(url_for('index'))

        comment = Comment(content = request.form["contents"])
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/login/', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        return render_template("login_page.html", error=False)

    else:
        username = request.form["username"]
        if username not in all_users:
            return render_template("login_page.html", error=True)
        else:
            user = all_users[username]
            if not user.check_password(request.form["password"]):
                return render_template("login_page.html", error=True)

            else:
                login_user(user)
                return redirect(url_for('index'))


@app.route('/logout/', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))





