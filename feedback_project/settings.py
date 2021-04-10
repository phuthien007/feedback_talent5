from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Thienphu1@localhost/talent5_feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = "\xeaH\x19p+\xd3\xa5\xac\xd1N\xed\x99v\x89;dFwp\xee\xa4\xaf\xff\x0b\xbc\x04\xc2\xe6o\xaa\xd9\xf5\xf2\x98\xb4zT*\x88\xe8\x136\xb3\xaa\x90\x9f6^\x00V\x9a\x18eZcK6=\xe7\x9f\xe0*[\xfelV\x85\xe4~\x9cp6\xc9\n\x02\xfdC#\x03\xf7\x16%wC\xdf\xaf\xbfe\xc5-S_\x0b\x03D\x0eR>8\xb6z\xa6\x93V\x95\x85f7\xc3\xb9\xc7\x95%+>B\xfa\xb1'\x90\xa7\xe6\xdf\x0e\xea4\xeeb"
db = SQLAlchemy(app)
# engine = create_engine('postgresql://postgres:Thienphu1@localhost/talent5_feedback')
login_manager= LoginManager(app=app)
login_manager.login_view= '/admin/'

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'phailamsaonana@gmail.com',
    "MAIL_PASSWORD": 'Nhutaikhoan'
}

app.config.update(mail_settings)
mail = Mail(app)
