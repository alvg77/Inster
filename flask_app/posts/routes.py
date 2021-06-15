from flask import render_template, flash, redirect, url_for, request, abort, Blueprint, current_app
from flask_login import current_user, login_required
from flask_app import db
from flask_app.models import User, Posts, Comments
from flask_app.posts.utils import save_post_pic
import os
from flask_app.posts.forms import PostForm, CommentsForm, ActionForm


posts = Blueprint('posts', __name__)

@posts.route('/post/new', methods=['POST', 'GET'])
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
        return redirect(url_for('main.home'))
    return render_template('new_post.html', title='New Post', form=form, user=current_user, header='New Post', post=None)

@posts.route("/post/<int:post_id>", methods=['POST', 'GET'])
@login_required
def post(post_id):
    post = Posts.query.get_or_404(post_id)
    likes = len(post.likes)
    form = CommentsForm()
    if form.validate_on_submit():
        comment = Comments(content=form.content.data, user_id=current_user.id, post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        flash('Comment successfully created!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
        
    return render_template('post.html', title=post.title, post=post, user=current_user, form=form, likes=likes)

@posts.route('/post/<int:post_id>/update', methods=['POST', 'GET'])
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
                os.remove(os.path.join(current_app.root_path, 'static/post_pics', post.post_image))
            post.post_image = filename         
        db.session.commit()
        flash('Your post has been updated!', 'success')
        
        return redirect(url_for('posts.post', post_id=post.id))
    
    elif request.method == 'GET':      
        form.title.data = post.title
        form.content.data = post.content

    return render_template('new_post.html', title='Update Post', form=form, user=current_user, header='Update Post', post=post)

@posts.route('/post/<int:post_id>/update/delete_img', methods=['POST', 'GET'])
@login_required
def delete_img(post_id):
    post = Posts.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    picture_path = os.path.join(current_app.root_path, 'static/post_pics', post.post_image)
    os.remove(picture_path)
    post.post_image = None
    db.session.commit()
    
    return redirect(url_for('posts.update_post', post_id=post_id))

@posts.route('/post/<int:post_id>/delete', methods=['Post'])
def delete_post(post_id):
    post = Posts.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    if post.post_image:
        picture_path = os.path.join(current_app.root_path, 'static/post_pics', post.post_image)
        os.remove(picture_path)
    for i in post.comments:
        db.session.delete(i)
    
    db.session.delete(post)
    db.session.commit()
    flash("Post successfully deleted!", "success")
    
    return redirect(url_for('main.home'))

@posts.route('/post/<int:post_id>/comment/<int:comment_id>/delete')
def delete_comment(post_id, comment_id):
    comment = Comments.query.get_or_404(comment_id)
    if comment.author != current_user:
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    flash('Comment successfully deleted!', 'success')
    
    return redirect(url_for('posts.post', post_id=post_id))

@posts.route("/post/<int:post_id>/like", methods=['POST'])
@login_required
def like(post_id):
    form = ActionForm()
    if form.validate_on_submit():
        post = Posts.query.get_or_404(post_id)
        current_user.like_post(post)
        db.session.commit()
        
        return redirect(url_for('posts.post', post_id=post_id))
    else:
        return redirect(url_for('main.home'))

@posts.route("/post/<int:post_id>/unlike", methods=['POST'])
@login_required
def unlike(post_id):
    form = ActionForm()
    if form.validate_on_submit():
        post = Posts.query.get_or_404(post_id)
        current_user.unlike_post(post)
        db.session.commit()

        return redirect(url_for('posts.post', post_id=post_id))
    else:
        return redirect(url_for('main.home'))