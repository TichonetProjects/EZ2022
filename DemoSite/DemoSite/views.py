"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, redirect, url_for
from DemoSite import app
import sqlite3
from sqlite3 import Error
from flask_login import login_user, current_user, logout_user, login_required


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
        return render_template(
        'register.html',
        title='Register',
        year=datetime.now().year,
        message='Resgister Page.'
    )

@app.route('/redirection', methods=['POST'])
def redirection():
    name = request.form.get("name")
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")
    try:
        conn = sqlite3.connect(r"database.db")
        print("Connection is being made!")
        cursor = conn.cursor()
        cursor.execute('SELECT EXISTS(SELECT 1 FROM users WHERE username=?);', (username,))
        
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (name, email, username, password))
            success = True
        else:
            print("this user already exists!")
            success = False
            return render_template(
             'error.html',
            title='Error',
            year=datetime.now().year,
            message='Error Page.',
            error='משתמש עם שם משתמש זהה קיים כבר. אנא נסה שם משתמש אחר.'
             )

        conn.commit()
        conn.close()

    except Error as e:
        print(e)
    finally:

        if success:
            return redirect(url_for('profile'))



@app.route('/profile')
# @login_required
def profile():
        return render_template(
        'profile.html',
        title='Profile',
        year=datetime.now().year,
        message='Profile Page.',
    )