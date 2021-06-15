from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, TextAreaField
from flask_app.models import User
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=25)])
    confirm = PasswordField('Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("Username unavailable! Please choose a different one.")
        
        username = username.data
        if not username.isalnum():
            raise ValidationError("Username can contain only letters and numbers")
    
    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Email unavailable! Please choose a different one.")
    
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField("Login")

    def validate_email(self, email):
        if not User.query.filter_by(email=email.data).first():
            raise ValidationError("No user with such email registered!")
        
class EditAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    bio = TextAreaField('Bio', validators=[Length(max=200)])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Apply changes')
    
    def validate_username(self, username):
        if username.data != current_user.username:
            if User.query.filter_by(username=username.data).first():
                raise ValidationError("Username unavailable! Please choose a different one.")

    def validate_email(self, email):
        if email.data != current_user.email:
            if User.query.filter_by(email=email.data).first():
                raise ValidationError("Email unavailable! Please choose a different one.")
            
class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first() is None:
            raise ValidationError("There is no account with that email. You must register first.")    

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=25)])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
    
class SearchForm(FlaskForm):
    search = StringField('Search', validators=[Length(min=3)])
    submit = SubmitField('Search')
    
class ActionForm(FlaskForm):
    submit = SubmitField('Action')