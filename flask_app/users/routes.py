from flask_app.users.utils import UserAuth, UserSignUp, save_picture, send_email_reset
import os
from flask_app.models import User
from flask import current_app, render_template, flash, redirect, url_for, request, abort, Blueprint
from flask_app.users.forms import (SignupForm, LoginForm, EditAccountForm,
                              ActionForm, RequestResetForm, 
                             ResetPasswordForm, SearchForm)
from flask_app import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
users = Blueprint('users', __name__)

@users.route('/people', methods=['POST', 'GET'])
@login_required
def people():
    page = request.args.get('page', 1, type=int)
    users = current_user.followed.paginate(page=page, per_page=8)
    
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('main.search', searched=form.search.data, type=0))
    return render_template('content.html', type='users', data=users, form=form, title='People', all=True, heading='Followed Users', none_message="No users followed")

@users.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    else: 
        form = LoginForm()
        if form.validate_on_submit():
            if UserAuth(form.email.data, form.password.data):
                login_user(User.query.filter_by(email=form.email.data).first(), remember=form.remember.data)
                next_page = request.args.get('next')
                print(request.args)
                flash('Your have successfully signed in!', category='success')
                
                return redirect(next_page) if next_page else redirect(url_for('main.home'))
            else:
                flash('Login failed! Please check your credentials!', category='danger')
        
        return render_template('login.html', title="Login", form=form)

@users.route('/signup', methods=['POST', 'GET'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    else:    
        form = SignupForm()
        if form.validate_on_submit():
            password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            UserSignUp(form.username.data, form.email.data, password)
            flash("Account created successfully!", "success")        
            return redirect(url_for('users.login'))
        
        return render_template('signup.html', title="Sign Up", form=form)

@users.route('/logout')
def logout():
    logout_user()
    
    return redirect(url_for('main.home'))

@users.route('/account', methods=['POST', 'GET'])
@login_required
def account():
    if not os.path.exists(os.path.join(current_app.root_path, 'static/profile_pics', current_user.profile_image)):
        current_user.profile_image = 'default.jpg'
    form = EditAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            if current_user.profile_image != 'default.jpg':
                os.remove(os.path.join(current_app.root_path, 'static/profile_pics', current_user.profile_image))
            current_user.profile_image = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        db.session.commit()
        flash('Account changes have been applied.', category='success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.bio
        
    return render_template('account.html', current_user=current_user, user=current_user, form=form, num_of_posts=len(current_user.posts), title=current_user.username)

@users.route("/user/<int:user_id>")
def user(user_id):
    user = User.query.get_or_404(user_id)
    if user == current_user:
        return redirect(url_for('users.account'))
    
    form = ActionForm()
    
    return render_template('account.html', title=user.username, current_user=current_user, user=user, image_file=user.profile_image, num_of_posts=len(user.posts), form=form)

@users.route("/user/<string:username>/followers", methods=['POST', 'GET'])
@login_required
def followers(username):
    user = User.query.filter_by(username=username).first()
    
    if not user:
        abort(404)
    else:
        page = request.args.get('page', 1, type=int)
        followers = user.followers.paginate(page=page, per_page=20)         
        return render_template('content.html', form=None, data=followers, type='users', title='Followers', all=False, heading="Followers", none_message="This user has no followers")

@users.route("/user/<string:username>/followed", methods=['POST', 'GET'])
@login_required
def followed(username):
    user = User.query.filter_by(username=username).first()
    
    if not user:
        abort(404)
    else:
        page = request.args.get('page', 1, type=int)
        followers = user.followed.paginate(page=page, per_page=20)
        return render_template('content.html', form=None, data=followers, type='users', title='Followers', all=False, heading="Followed", none_message="This user hasn't followed anyone")
    
@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_email_reset(user)
        flash('An email to reset your password has been sent.', 'info')
        return redirect(url_for('users.login'))
        
    return render_template('request.html', title='Reset Password', form=form)

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    
    if not user:
        flash('Token is invalid or expired!', 'warning')
        return redirect(url_for('users.reset_request'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = password
        db.session.commit()
        flash("Your password has been updated!", "success")        
        
        return redirect(url_for('users.login'))
        
    return render_template('reset.html', title='Reset Password', form=form)

@users.route('/follow/<user_username>', methods=['POST', 'GET'])
@login_required
def follow(user_username):
    form = ActionForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=user_username).first()
        if user == None:
            flash(f"User {user_username} doesn't exist.", 'info')
            return redirect(url_for('main.home'))
        if user == current_user:
            flash('You cannot follow yourself!', 'danger')
            return redirect(url_for('users.account'))
        current_user.follow(user)
        db.session.commit()
        flash(f'You are now following {user.username}.', 'info')
        return redirect(url_for('users.user', user_id=user.id))
    else:
        return redirect(url_for('main.home'))


@users.route('/unfollow/<user_username>', methods=['POST', 'GET'])
@login_required
def unfollow(user_username):
    form = ActionForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=user_username).first()
        if user == None:
            flash(f"User {user_username} doesn't exist.", 'info')
            return redirect(url_for('main.home'))
        if user == current_user:
            flash('You cannot unfollow yourself!', 'danger')
            return redirect(url_for('users.account'))
        current_user.unfollow(user)
        db.session.commit()
        flash(f'You have unfollowed user {user.username}.', 'info')
        
        return redirect(url_for('users.user', user_id=user.id))
    else:
        return redirect(url_for('main.home'))
    
@users.route('/<user_id>/delete_user/', methods=['POST', 'GET'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    for i in user.posts:
        if i.post_image:
            image_path = os.path.join(current_app.root_path, 'static/post_pics', i.post_image)
            os.remove(image_path)
        i.query.delete()
    user.query.delete()
    db.session.commit()
    logout()
    
    return redirect(url_for('users.login'))