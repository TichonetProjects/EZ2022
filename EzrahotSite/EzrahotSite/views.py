"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, redirect, url_for
from EzrahotSite import app, db, bcrypt
import sqlite3
from sqlite3 import Error
from flask_login import login_user, current_user, logout_user, login_required

from EzrahotSite.models import User

from EzrahotSite.forms import RegistrationForm



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

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Renders the login page."""
    return render_template(
        'login.html',
        title='Login',
        year=datetime.now().year,
        message='Login Page.'
    )

@app.route('/register', methods=['GET', 'POST'])
def register():
        form = RegistrationForm()
        return render_template(
        'register.html',
        title='Register',
        year=datetime.now().year,
        message='Resgister Page.',
        form = form
    )

@app.route('/redirection', methods=['GET', 'POST'])
def redirection():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")
    school_class = request.form.get("school_class")
    try:
    

        new_user = User(user_id = 1, first_name = first_name, last_name = last_name, email = email, password = password, school_class = school_class, user_type = "Waiting_For_Accept" )
        
        db.session.add(new_user)
        db.session.commit()
    except Error as e:
         print(e)
    finally:
        return redirect(url_for('home'))



@app.route('/profile')
@login_required
def profile():
        return render_template(
        'profile.html',
        title='Profile',
        year=datetime.now().year,
        message='Profile Page.',
    )