"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, redirect, url_for, flash, Response, abort
from EzrahotSite import app, db, bcrypt#, md
import sqlite3
from sqlite3 import Error
from flask_login import login_user, current_user, logout_user, login_required

from EzrahotSite.models import User, Article

from EzrahotSite.forms import RegistrationForm, LoginForm, SubmitArticle

#from flask_misaka import markdown


@app.route('/')
@app.route('/home')
def home():
    acceptedArticles = Article.get_all_active()
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
        articles=acceptedArticles
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
        message='Your application description page.',
        mkd_text=""
    )


@app.route('/test')
def test():
    """Renders the about page."""

    test_text =  "## הנה זה טקסט בעברית! <br> ![alt text](https://github.com/laynH/Anime-Girls-Holding-Programming-Books/blob/master/C/Hakurei_Reimu_Holding_C_Programming_Language.jpg?raw=true)"
   

    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.',
        mkd_text=md.render(test_text)
        )


@app.route('/register', methods=['GET', 'POST'])
def register():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        form = RegistrationForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, password=hashed_password, school_class=form.school_class.data, user_type="Wating_For_Aprrove")

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
        if user != None and bcrypt.check_password_hash(user.password, form.password.data) and user.is_active():
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        elif (not user == None) and not user.is_active():
            flash('המשתמש הזה עדיין לא אושר על ידי מנהל. נסה שוב מאוחר יותר', 'danger')
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

@app.route('/submit-article', methods=['GET', 'POST'])
@login_required
def submitArticle():
    form = SubmitArticle()
    if form.validate_on_submit():
        article = Article(heading=form.heading.data, body=form.body.data, post_date=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), accept_date=None, is_accepted=False, author_id=current_user.user_id)

        db.session.add(article)
        db.session.commit()

        flash('הפוסט נוצר בהצלחה וממתין לאישור מנהל.', 'success')

        return redirect(url_for('articles', index=article.article_id))

    return render_template('submitArticle.html', year=datetime.now().year, form=form)

@app.route('/control-panel')
@login_required
def controlPanel():
    return render_template('controlPanel.html', year=datetime.now().year, inactiveUsers = User.get_all_inactive())

@app.route('/article/<index>/')
def articles(index):
    article = Article.query.filter_by(article_id=index).first()
    
    if article is None:
        abort(404, description="Resource not found")
    author = User.query.filter_by(user_id=article.author_id).first()
    return render_template('articles.html', year=datetime.now().year, articleBody="")#md.render(article.body), articleHeading=article.heading, Articleauthor=f"{author.first_name} {author.last_name}")

@app.errorhandler(404)
def not_found(exc):
    return Response(render_template('404.html', title="Page Not Found")), 404