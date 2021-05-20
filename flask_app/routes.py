from flask_app.models import User, Posts 
from flask import render_template, flash, redirect, url_for, request
from flask_app.forms import SignupForm, LoginForm
from flask_app import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

posts = [
    {
        "author": "dasdsa",
        "title": "Neshto toxic",
        "date": "06.09.2420",
        "Content": "asdasdasdashegrqhteh    3   532HGGWEDQW",
    }
]

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
    return render_template('home.html', title="suffer", data=posts, image=None)

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
                print('\n\n\n\n\n\n')
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

@app.route('/account')
@login_required
def account():

    return render_template('account.html', user=current_user)
