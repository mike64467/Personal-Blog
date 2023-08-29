import os
from flask import render_template, url_for, request, redirect, flash
from blog import app, db, login_manager
from blog.models import User, Post, Comment
from blog.forms import RegistrationForm, LoginForm, PostForm, CommentForm
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
# from wtforms import StringField,PasswordField,SubmitField, FileField

@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/post/<int:post_id>")
def post(post_id):
    form = CommentForm()
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post_id).all()
    return render_template('post.html', post=post, form=form, comments=comments)


@app.route('/create-post', methods=['GET', 'POST'])
@login_required
def create():
  form = PostForm()
  if request.method == 'POST':
    # title = request.form.get('title')
    # content = request.form.get('content')
    # file = request.form.get('file')
    title, content, image = form.title.data, form.content.data, form.file.data

    author_id = current_user.id 
    # file = file.filename

    filename = secure_filename(image.filename)
    basedir = os.path.abspath(os.path.dirname(__file__))
    image.save(os.path.join(basedir, './static/img', filename))

    # file.save(url_for('static/img', filename=filename))
    new_post = Post(title=title, content=content,image_file = filename , author_id=author_id)
    db.session.add(new_post)
    db.session.commit()
    flash('Post sent', 'success')
    return redirect(url_for('home'))

  return render_template('create.html', user=current_user, form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        print("validated")
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        print("registered")
        flash('Registration successful!', 'success')
        return redirect(url_for('registered'))
    return render_template('register.html', title='Register', form=form)


@app.route("/registered")
def registered():
    return render_template('registered.html', title='Thanks!')


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            flash('You\'ve successfully logged in,' + ' ' + current_user.username + '!', 'success')
            return redirect(url_for('home'))
        flash('Invalid username or password.', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user()
    flash('You\'re now logged out. Thanks for your visit!', 'success')
    return redirect(url_for('home'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/comment/<int:post_id>", methods=['POST'])
@login_required
def comment(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        # author_id = current_user.id
        # user = User.query.filter_by(username=form.username.id)
        comment = Comment(content = form.content.data, author_id = current_user.id, post_id = post_id)
        db.session.add(comment)
        db.session.commit()
        flash('You\'re now posted your comment', 'success')
        return redirect(url_for('post', post_id=post_id))
    flash('You\'re failed to post your comment, please try again', 'danger')
    return redirect(url_for('post',post_id=post_id))
    

# @app.route("/post/<int:post_id>")
# def post(post_id):
#     post = Post.query.get_or_404(post_id)
#     return render_template('post.html', title=post.title, post=post)
    
    