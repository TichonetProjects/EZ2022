"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, redirect, url_for, flash
from EzrahotSite import app, db, bcrypt
import sqlite3
from sqlite3 import Error
from flask_login import login_user, current_user, logout_user, login_required

from EzrahotSite.models import User

from EzrahotSite.forms import RegistrationForm, LoginForm

import random


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )


@app.route('/register', methods=['GET', 'POST'])
def register():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        form = RegistrationForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(user_id=random.randint(1, 1000000), first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, password=hashed_password, school_class=form.school_class.data, user_type="Wating_For_Aprrove")

            db.session.add(user)
            db.session.commit()

            flash('המשתמש נוצר בהצלחה. המתן לאישורו, לאחר האישור יהיה ניתן להתחבר עם המשתמש לאתר.', 'success')

            return redirect(url_for('login'))
            
        return render_template(
        'register.html',
        title='Register',
        year=datetime.now().year,
        message='Resgister Page.',
        form = form
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user != None and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('ההתחברות נכשלה. אנא נסה שוב', 'danger')
    return render_template(
        'login.html',
        title='Login',
        year=datetime.now().year,
        message='Login Page.',
        form=form
    )

@app.route('/profile')
@login_required
def profile():
        return render_template(
        'profile.html',
        title='Profile',
        year=datetime.now().year,
        message='Profile Page.',
    )

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))