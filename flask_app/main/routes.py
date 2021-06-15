from flask import render_template, flash, redirect, url_for, request, abort, Blueprint
from flask_login import current_user, login_required
from flask_app.models import User, Posts
from flask_app.main.forms import SearchForm

main = Blueprint('main', __name__)

@main.route('/', methods=['POST', 'GET'])
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(page=page, per_page=8)
    form = SearchForm()
    if form.validate_on_submit():        
        return redirect(url_for('main.search', searched=form.search.data, type=1))
    
    return render_template('content.html', heading='Posts', title="Home", type='post', data=posts, form=form)

@main.route('/search/<searched>/<int:type>')
@login_required
def search(searched, type):
    
    if type == 1:
        data = Posts.query.whooshee_search(str(searched)).order_by(Posts.id.desc()).all()
    elif type == 0:
        data = User.query.whooshee_search(str(searched)).order_by(User.id.desc()).all()
        
    return render_template('search.html', data=data, type=type, title='Search')
