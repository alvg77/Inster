import os
import secrets
from PIL import Image
from flask_app import db, bcrypt, mail
from flask_mail import Message
from flask import url_for, current_app
from flask_app.models import User

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, extention = os.path.splitext(form_picture.filename)
    filename = random_hex + extention
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', filename)
    
    size = (155, 155)
    image = Image.open(form_picture)
    image.thumbnail(size)
    image.save(picture_path)    
    
    return filename

def send_email_reset(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', 
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, click on the following link:
{url_for('users.reset_token', token=token, _external=True)}

If it wasn't you who made this password reset request, simply ignore this email and no changes to your password will be made.
'''
    mail.send(msg)
    
def UserAuth(email, password):
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        return True
    
    return False    

def UserSignUp(username, email, password):
    new_user = User(username=username, email=email, password=password)
        
    db.session.add(new_user)
    db.session.commit()    