from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired, Length, Email,EqualTo,ValidationError
from flask_login import current_user
from flaskblog.models import User

class SignUpForm(FlaskForm):
    username = StringField('Username',
    validators = [DataRequired(),Length(min=2,max=50)])

    email = StringField('Email',
    validators = [DataRequired(),Email()]
    )

    password = PasswordField('Password',validators= [DataRequired()])

    password_confirm  = PasswordField('Confirm Password',validators = [DataRequired(),EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists ')

    def validate_email(self,email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email already exists ')


class LoginForm(FlaskForm):
   

    email = StringField('Email',
    validators = [DataRequired(),Email()]
    )

    password = PasswordField('Password',validators= [DataRequired()])

    remember= BooleanField('Remeber Me')

    submit = SubmitField('Sign In')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
    validators = [DataRequired(),Length(min=2,max=50)])

    email = StringField('Email',
    validators = [DataRequired(),Email()]
    )

    pic  = FileField('Update Profile Pic', validators = [FileAllowed(['jpg','png'])])

    submit = SubmitField('Update')

    def validate_username(self,username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already exists ')

    def validate_email(self,email):
        if email.data != current_user.username:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('Email already exists ')

class RequestResetForm(FlaskForm):
    email = StringField('Email',validators = [DataRequired(),Email()])

    submit = SubmitField('Request password reset')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user is None:
            raise ValidationError('Account does not exists ')

class ResetPasswordForm(FlaskForm):
    
    password = PasswordField('Password',validators= [DataRequired()])

    password_confirm  = PasswordField('Confirm Password',validators = [DataRequired(),EqualTo('password')])

    submit = SubmitField('Reset password')
