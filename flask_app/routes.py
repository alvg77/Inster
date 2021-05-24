import os
import secrets
from PIL import Image
from flask_app.models import User, Posts, Comments
from flask import render_template, flash, redirect, url_for, request, abort
from flask_app.forms import SignupForm, LoginForm, EditAccountForm, PostForm, CommentsForm
from flask_app import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

def UserAuth(email, password):
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        return True
    
    return False    
    

def UserSignUp(username, email, password):
    new_user = User(username=username, email=email, password=password)
        
    db.session.add(new_user)
    db.session.commit()         

@app.route('/')
@app.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Posts.query.order_by(Posts.date_posted.desc()).paginate(page=page, per_page=8)
        
    return render_template('home.html',  title="suffer", data=posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    else: 
        form = LoginForm()
        if form.validate_on_submit():
            if UserAuth(form.email.data, form.password.data):
                login_user(User.query.filter_by(email=form.email.data).first(), remember=form.remember.data)
                next_page = request.args.get('next')
                print(request.args)
                flash('Your have successfully signed in!', category='success')
                
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash('Login failed! Please check your credentials!', category='danger')
        
        return render_template('login.html', title="Login", form=form)

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    else:    
        form = SignupForm()
        if form.validate_on_submit():
            password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            UserSignUp(form.username.data, form.email.data, password)
            flash("Account created successfully!", "success")        
            return redirect(url_for('login'))
        
        return render_template('signup.html', title="Sign Up", form=form)

@app.route('/logout')
def logout():
    logout_user()
    
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, extention = os.path.splitext(form_picture.filename)
    filename = random_hex + extention
    picture_path = os.path.join(app.root_path, 'static/profile_pics', filename)
    
    size = (155, 155)
    image = Image.open(form_picture)
    image.thumbnail(size)
    image.save(picture_path)    
    
    return filename

@app.route('/account', methods=['POST', 'GET'])
@login_required
def account():
    if not os.path.exists(os.path.join(app.root_path, 'static/profile_pics', current_user.profile_image)):
        current_user.profile_image = 'default.jpg'
    form = EditAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            if current_user.profile_image != 'default.jpg':
                os.remove(os.path.join(app.root_path, 'static/profile_pics', current_user.profile_image))
            current_user.profile_image = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        db.session.commit()
        flash('Account changes have been applied.', category='success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.bio
        
    return render_template('account.html', current_user=current_user, user=current_user, form=form, num_of_posts=len(current_user.posts))

def save_post_pic(image):
    random_hex = secrets.token_hex(8)
    _, extention = os.path.splitext(image.filename)
    filename = random_hex + extention
    picture_path = os.path.join(app.root_path, 'static/post_pics', filename)

    image = Image.open(image)
    image.save(picture_path)    
    
    return filename

@app.route('/post/new', methods=['POST', 'GET'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        if form.image.data:
            filename = save_post_pic(form.image.data)
        else:
            filename = None
        post = Posts(title=form.title.data, content=form.content.data, post_image=filename, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('new_post.html', title='New Post', form=form, user=current_user, header='New Post', post=None)

@app.route("/post/<int:post_id>", methods=['POST', 'GET'])
def post(post_id):
    post = Posts.query.get_or_404(post_id)
    form = CommentsForm()
    if form.validate_on_submit():
        comment = Comments(content=form.content.data, user_id=current_user.id, post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        flash('Comment successfully created!', 'success')
        return redirect(url_for('post', post_id=post.id))
        
    return render_template('post.html', title=post.title, post=post, user=current_user, form=form)

@app.route('/post/<int:post_id>/update', methods=['POST', 'GET'])
@login_required
def update_post(post_id):
    post = Posts.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    form.title.data = post.title
    form.content.data = post.content
    
    if post.post_image == 'removed':
            post.post_image = None  
             
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data

        if form.image.data:
            filename = save_post_pic(form.image.data)
            if post.post_image:
                os.remove(os.path.join(app.root_path, 'static/post_pics', post.post_image))
            post.post_image = filename         
        db.session.commit()
        flash('Your post has been updated!', 'success')
        
        return redirect(url_for('post', post_id=post.id))
    
    elif request.method == 'GET':      
        form.title.data = post.title
        form.content.data = post.content

    return render_template('new_post.html', title='Update Post', form=form, user=current_user, header='Update Post', post=post)

@app.route('/post/<int:post_id>/update/delete_img', methods=['POST', 'GET'])
@login_required
def delete_img(post_id):
    post = Posts.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    picture_path = os.path.join(app.root_path, 'static/post_pics', post.post_image)
    os.remove(picture_path)
    post.post_image = 'removed'
    db.session.commit()
    
    return redirect(url_for('update_post', post_id=post_id))

@app.route('/post/<int:post_id>/delete', methods=['Post'])
def delete_post(post_id):
    post = Posts.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    if post.post_image:
        picture_path = os.path.join(app.root_path, 'static/post_pics', post.post_image)
        os.remove(picture_path)
    for i in post.comments:
        db.session.delete(i)
    
    db.session.delete(post)
    db.session.commit()
    flash("Post successfully deleted!", "success")
    
    return redirect(url_for('home'))

@app.route("/user/<int:user_id>")
def user(user_id):
    user = User.query.get_or_404(user_id)
    if user == current_user:
        return redirect(url_for('account'))
    
    return render_template('account.html', current_user=current_user, user=user, image_file=user.profile_image, num_of_posts=len(user.posts))

@app.route('/post/<int:post_id>/comment/<int:comment_id>/delete')
def delete_comment(post_id, comment_id):
    comment = Comments.query.get_or_404(comment_id)
    if comment.author != current_user:
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    flash('Comment successfully deleted!', 'success')
    
    return redirect(url_for('post', post_id=post_id))