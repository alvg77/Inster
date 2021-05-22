from flask_app.models import User
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_login import current_user

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=25)])
    confirm = PasswordField('Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("Username unavailable! Please choose a different one.")

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Email unavailable! Please choose a different one.")
    
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField("Login")

class EditAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=25)])
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

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=25)])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])    
    content = TextAreaField('Content', validators=[DataRequired(), Length(max=200)])
    submit = SubmitField('Post')

