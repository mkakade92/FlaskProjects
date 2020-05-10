from flask import render_template,url_for,flash,redirect,request,Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (
    SignUpForm,
    LoginForm,
    RequestResetForm,
    ResetPasswordForm,
    UpdateAccountForm
)
from flaskblog.users.utils import save_pic, send_reset_email

users = Blueprint('users',__name__)

@users.route('/signup',methods = ['GET','POST'])
def signup():
   
    if current_user.is_authenticated:
       return redirect(url_for('main.home'))
    form = SignUpForm()

    if form.validate_on_submit():
        Hp = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username =form.username.data,email = form.email.data,password=Hp)
        db.session.add(user)
        db.session.commit()
        flash(f'Account Created for {form.username.data} !','success')
        return redirect(url_for('users.login'))
    return render_template('signup.html',title = 'Sign Up',form = form)

@users.route('/login',methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
       return redirect(url_for('main.home'))
    form = LoginForm()  
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
          login_user(user,remember=form.remember.data)
          next_page = request.args.get('next')
          return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
         flash(f'Incorrect Email or Password','danger')
    return render_template('login.html', title = 'Login', form=form)


@users.route('/logout')
def logout():
   logout_user()
   return redirect(url_for('main.home'))


@users.route('/account',methods = ['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
       if form.pic.data :
        picture_f = save_pic(form.pic.data) #this needs to be checked
        current_user.image_file = picture_f
       current_user.username = form.username.data
       current_user.email = form.email.data
       db.session.commit()
       flash(f'Your Account has been updated','success')
       return redirect(url_for('users.account'))
    
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static',filename='profile_pics/'+current_user.image_file)
    return render_template('account.html',title ='Account',image_file=image_file ,form=form)

@users.route("/user/<string:username>/posts")
def user_posts(username):
    page = request.args.get('page',1,type = int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page,per_page=5)
    return render_template("user_posts.html",posts=posts,user=user)


@users.route('/reset_password',methods=['GET','POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form =RequestResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent woth instructions to reset the password','info')
        return redirect(url_for('users.login'))
    return render_template(
        'reset_request.html',
        title=  'Reset Password',
        form =form  
    )

@users.route('/reset_password/<token>',methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)

    if not user:
        flash('That is invalid or expired token','warning')
        return redirect(url_for('users.reset_password'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        Hp = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password=Hp
        db.session.commit()
        flash(f'Password Reset for {user.usernamecle} !','success')
        return redirect(url_for('users.login'))
    return render_template(
       'reset_token.html',
       title='Reset Password',
       form = form
    ) 