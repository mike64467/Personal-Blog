from flask_wtf import FlaskForm
# from flask_wtf.file import FeilField, FileRequired
from wtforms import StringField,PasswordField,SubmitField, FileField
from wtforms.validators import DataRequired,ValidationError,Regexp,EqualTo
from blog.models import User
from flask import flash

#注册表格，加上注册账号长度和小写限制规则
class RegistrationForm(FlaskForm):
  username = StringField('Username')
  password = PasswordField('Password',validators=[DataRequired(),Regexp('^(?![0-9]+$)(?![a-z]+$)[a-z0-9]{6,16}$',message='Your password should be between 6 and 16 characters long, and contain numbers and lowercase letters.'),
                                                    EqualTo('confirm_password', message='Password do not match. Try again')])
  confirm_password = PasswordField('Confirm your Password',validators=[DataRequired()])  ####加上验证两次密码是否正确
  submit = SubmitField('Register')
  
  #check if username already exists, flash
  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user is not None:
      print("already exist" )
      flash('Username already exist. Please choose a different one.', 'danger')
      raise ValidationError('Username already exist. Please choose a different one.')

class LoginForm(FlaskForm):
  username = StringField('Username',validators=[DataRequired()])
  password = PasswordField('Password',validators=[DataRequired()])
  submit = SubmitField('Login')

class PostForm(FlaskForm):
  title = StringField('Tite', validators=[DataRequired()])
  content = StringField('Content', validators=[DataRequired()])
  file = FileField("File")
  submit = SubmitField('Post')
  
class CommentForm(FlaskForm):                 #表格的框架
  content = StringField('Content', validators=[DataRequired()])
  submit = SubmitField('Post')