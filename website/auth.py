from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if(request.method == 'POST'):
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash("Users login successfully", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Password incorrect, please try again", category='error')
        else :
            flash("User not found", category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if(request.method == 'POST'):
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password = request.form.get('password1')
        confirm_password = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        
        if user :
            flash('User already exists', category='error')
        elif(len(email) < 4):
            flash('Email must be at least 3 characters', category='error')

        elif(len(first_name) < 2):
            flash('Firstname must be at least 1 characters', category='error')

        elif password != confirm_password:
            flash('Password must be the same as the confirm password', category='error')

        elif(len(password) < 7):
            flash('Password must be at least 6 characters', category='error')

        else:
            new_user = User(email=email, password=generate_password_hash(password,method='pbkdf2', salt_length=10))
            print(new_user)
            db.session.add(new_user)
            db.session.commit()
            flash('User created', category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
        
    return render_template("sign_up.html", user=current_user)