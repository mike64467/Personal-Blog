import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = '<03391a09e27cd8f3704d0234fd1099c7c285a5cef0eb17b2>'
app.config['SQLALCHEMY_DATABASE_URI'] =  'mysql+pymysql://ASDFGHHJKL:QWERTYUI@csmysql.cs.cf.ac.uk:3306/c21095796_ZiyeZhang_database1'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)



from blog import routes

from flask_admin import Admin
from blog.views import AdminView
from blog.models import User, Post, Comment
admin = Admin(app,name='Admin panel',template_mode='bootstrap3')
admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Post, db.session))
admin.add_view(AdminView(Comment, db.session))
