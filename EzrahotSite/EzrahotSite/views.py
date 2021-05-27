"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, redirect, url_for, flash, Response, abort
from EzrahotSite import app, db, bcrypt, md, mail
import sqlite3
from sqlite3 import Error
from flask_login import login_user, current_user, logout_user, login_required

from EzrahotSite.models import User, Article, admin_required, clean_string, acceptArticleMessage, acceptUserMessage, newArticleMessage, newUserMessage

from EzrahotSite.forms import RegistrationForm, LoginForm, SubmitArticle

from flask_mail import Mail, Message
import math


@app.route('/')
@app.route('/home')
def home():
    """renders the home page with all accepted articles"""
    acceptedArticles = Article.get_all_accepted()[:10]

    return render_template(
        'index.html',
        title='עמוד הבית',
        home_paragraph="מערכת עולם זכויות אדם",
        articles=acceptedArticles,
        len = len(acceptedArticles)
    )

@app.route('/articles-list/<index>/')
@app.route('/articles-list/')
def articlesview(index=1):
    """renders the articles page list with a specific page set"""
    index = int(index)-1
    articles_in_page = 5
    acceptedArticles = list(Article.get_all_accepted())
    pages_count = math.ceil(len(acceptedArticles)/articles_in_page)

    return render_template(
        'articlesview.html',
        title='רשימת הכתבות',
        articles=acceptedArticles[index*articles_in_page:(index+1)*articles_in_page],
        pages=map(lambda n:n+1, range(pages_count))
    )

@app.route('/contact')
def contact():
    """renders the contact page."""
    return render_template(
        'contact.html',
        title='צרו קשר',
        message='Your contact page.'
    )

@app.route('/devteam')
def devteam():
    """renders the dev team page"""
    return render_template('devteam.html', title="צוות הפיתוח")

@app.route('/register', methods=['GET', 'POST'])
def register():
    """renders the registration page"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        """whenever the form is submitted, enter the credentials into the database and hash the password""" 
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            first_name=clean_string(form.first_name.data), 
            last_name=clean_string(form.last_name.data), 
            email=clean_string(form.email.data), 
            password=hashed_password, 
            school_class=clean_string(form.school_class.data), 
            user_type="NOT_APPROVED")

        db.session.add(user)
        db.session.commit()

        """send an email to the admins about the new user"""
        msg = newUserMessage(user)
        mail.send(msg)


        flash('המשתמש נוצר בהצלחה. המתן לאישורו, לאחר האישור יהיה ניתן להתחבר עם המשתמש לאתר.', 'success')

        return redirect(url_for('login'))
        
    return render_template(
    'register.html',
    title='Register',
    message='דף הירשמות',
    form = form
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    """renders the login page"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        """whenver the form is submitted, check the credentials against the database and if they're correct login the user"""
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.is_active() and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))

        elif user and not user.is_active():
            flash('המשתמש הזה עדיין לא אושר על ידי מנהל. נסה שוב מאוחר יותר', 'danger')
        else:
            flash('ההתחברות נכשלה. אנא נסה שוב', 'danger')

    return render_template(
        'login.html',
        title='דף כניסה',
        
        message='Login Page.',
        form=form
    )

@app.route('/profile')
@login_required
def profile():
    """renders the profile page with all of the user's articles"""
    user_articles = Article.get_all_user(current_user.user_id)
    return render_template(
        'profile.html',
        title='עמוד כתב',
        message='Profile Page.',
        user_articles=user_articles
    )

@app.route('/logout')
@login_required
def logout():
    """logout endpoint for logging out users (must be logged in in order to access)"""
    logout_user()
    return redirect(url_for('home'))

@app.route('/edit-article/<index>/', methods=['GET', 'POST'])
@login_required
def editArticle(index):
    """renders the edit page article (must be logged and have ownership over the article in in order to access)"""
    article = Article.query.get(index)
    
    if not article or (not (current_user.is_authenticated and (current_user.user_id == article.author_id or current_user.is_admin()))):
        abort(404, description="Resource not found")
    
    form = SubmitArticle()
    form.submit.label.text = "שמור שינויים"

    if form.validate_on_submit():
        article.heading = clean_string(form.heading.data)
        # article.is_english = form.is_english.data
        article.body = clean_string(form.body.data)
        article.caption = clean_string(form.caption.data)
        article.thumbnail = clean_string(form.thumbnail.data) if clean_string(form.thumbnail.data) else "https://lh5.googleusercontent.com/p/AF1QipMF1XVDYrw7O7mg3E_fLqgAceacWExqaP4rbptz=s435-k-no"
  
        db.session.commit()

        flash('הכתבה עודכנה בהצלחה', 'success')

        return redirect(url_for('articles', index=article.article_id))

    elif request.method == 'GET':
        form.heading.data = article.heading
        form.caption.data = article.caption
        form.body.data = article.body
        form.thumbnail.data = article.thumbnail

    return render_template('submitArticle.html',  title="ערוך כתבה", form=form)

@app.route('/create-article/', methods=['GET', 'POST'])
@login_required
def createArticle():
    """renders the create article page (must be logged in in order to access)"""
    form = SubmitArticle()
    if form.validate_on_submit():
        article = Article(
            heading=clean_string(form.heading.data),
            body=clean_string(form.body.data),
            post_date=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            accept_date=None,
            is_accepted=False,
            # is_english=form.is_engish.data,
            author_id=current_user.get_id(),
            caption=clean_string(form.caption.data),
            thumbnail=clean_string(form.thumbnail.data) if clean_string(form.thumbnail.data) else "https://lh5.googleusercontent.com/p/AF1QipMF1XVDYrw7O7mg3E_fLqgAceacWExqaP4rbptz=s435-k-no")

        db.session.add(article)
        db.session.commit()

        msg = newArticleMessage(article)
        mail.send(msg)

        flash('הכתבה נוצרה בהצלחה וממתינה לאישור מנהל.', 'success')

        return redirect(url_for('articles', index=article.article_id))

    return render_template('submitArticle.html', title="צור כתבה חדשה", form=form)


@app.route('/control-panel')
@login_required
@admin_required
def controlPanel():
    """renders the control panel page with all unaccepted users and articles (must be logged in AND be an admin in order to access)"""
    inactiveUsers = list(User.get_all_inactive())
    inactiveArticles = list(Article.get_all_unaccepted())

    return render_template('controlPanel.html',  title="פאנל מנהלים", inactiveUsers = inactiveUsers, inactiveArticles = inactiveArticles, userstitle="אישור משתמשים", nousers="אין משתמשים שממתינים לאישור", articlestitle="אישור כתבות", noarticles="אין כתבות שממתינות לאישור")


@app.route("/acceptuser/<index>", methods=['GET', 'POST'])
@login_required
@admin_required
def acceptUser(index):
    """accept user endpoint for accepting new users (must be logged in AND be an admin in order to access)"""
    user = User.query.get(index)
    
    if user:
        user.accept_user()
        msg = acceptUserMessage(user)
        mail.send(msg)
    
    next_page = request.args.get('next')
    return redirect(url_for('controlPanel'))

@app.route("/deleteuser/<index>", methods=['GET', 'POST'])
@login_required
@admin_required
def deleteUser(index):
    """delete user endpoint for deleting existing users (must be logged in AND be an admin in order to access)"""
    user = User.query.get(index)

    if user:
        user.delete_user()

    next_page = request.args.get('next')
    return redirect(url_for('controlPanel'))

@app.route("/acceptarticle/<index>", methods=['GET', 'POST'])
@login_required
@admin_required
def acceptArticle(index):
    """accept article endpoint for accepting new articles (must be logged in AND be an admin in order to access)"""
    article = Article.query.get(index)

    if article:
        article.accept_article()
        msg = acceptArticleMessage(article)
        mail.send(msg)

    next_page = request.args.get('next')
    return redirect(next_page) if next_page else redirect(url_for('articlesview'))

@app.route("/deletearticle/<index>", methods=['GET', 'POST'])
@login_required
@admin_required
def deleteArticle(index):
    """delete article endpoint for deleting existing articles (must be logged in AND be an admin in order to access)"""
    article = Article.query.get(index)

    if article:
        article.delete_article()

    next_page = request.args.get('next')
    return redirect(next_page) if next_page else redirect(url_for('articlesview'))

@app.route('/article/<index>/')
def articles(index):
    """renders an article page"""
    article = Article.query.get(index)
    
    if not article:
        abort(404, description="Resource not found")
    
    elif not article.is_accepted:
        if not (current_user.is_authenticated and (current_user.user_id == article.author_id or current_user.is_admin())):
            abort(404, description="Resource not found")

    author = article.get_author()
    return render_template('articles.html', 
                        title=article.heading,
                        article=article,
                        articleBody=article.body,
                        articleAuthor=f"{author.first_name} {author.last_name}, {author.school_class}"
                        , direction ="ltr" if article.article_id == 24 else"rtl")


@app.errorhandler(404)
def not_found(exc):
    return Response(render_template('404.html', title="עמוד לא נמצא", text="404: העמוד לא נמצא :(")), 404