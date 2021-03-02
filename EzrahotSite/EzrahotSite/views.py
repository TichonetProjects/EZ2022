"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, redirect, url_for, flash, Response, abort
from EzrahotSite import app, db, bcrypt, md
import sqlite3
from sqlite3 import Error
from flask_login import login_user, current_user, logout_user, login_required

from EzrahotSite.models import User, Article, admin_required

from EzrahotSite.forms import RegistrationForm, LoginForm, SubmitArticle

from flask_misaka import markdown


@app.route('/')
@app.route('/home')
def home():
    """renders the home page with all accepted articles"""
    acceptedArticles = Article.get_all_accepted()

    return render_template(
        'index.html',
        title='Home Page',
        articles=acceptedArticles
    )

@app.route('/articles-list')
def articlesview():
    acceptedArticles = Article.get_all_accepted()

    return render_template(
        'articlesview.html',
        title='Articles',
        articles=acceptedArticles
    )

@app.route('/contact')
def contact():
    """renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """renders the about page."""
    return render_template(
        'about.html',
        title='About',
        message='Your application description page.',
    )

@app.route('/devteam')
def devteam():
    return render_template('devteam.html', title="Develpment Team")

@app.route('/register', methods=['GET', 'POST'])
def register():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        
        form = RegistrationForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(
                first_name=form.first_name.data, 
                last_name=form.last_name.data, 
                email=form.email.data, 
                password=hashed_password, 
                school_class=form.school_class.data, 
                user_type="NOT_APPROVED")

            db.session.add(user)
            db.session.commit()

            flash('המשתמש נוצר בהצלחה. המתן לאישורו, לאחר האישור יהיה ניתן להתחבר עם המשתמש לאתר.', 'success')

            return redirect(url_for('login'))
            
        return render_template(
        'register.html',
        title='Register',
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
        title='Login',
        
        message='Login Page.',
        form=form
    )

@app.route('/profile')
@login_required
def profile():
    user_articles = Article.get_all_user(current_user.user_id)
    return render_template(
        'profile.html',
        title='Profile',
        message='Profile Page.',
        user_articles=user_articles
    )

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/edit-article/<index>/', methods=['GET', 'POST'])
@login_required
def editArticle(index):
    article = Article.query.get(index)
    
    if not article or (not (current_user.is_authenticated and (current_user.user_id == article.author_id or current_user.is_admin()))):
        abort(404, description="Resource not found")

    form = SubmitArticle()
    form.heading.data = article.heading
    form.caption.data = article.caption
    form.body.data = article.body
    form.thumbnail.data = article.thumbnail

    if form.validate_on_submit():
        article = Article(
            heading=form.heading.data,
            body=form.body.data,
            post_date=article.post_date,
            accept_date=article.accept_date,
            is_accepted=article.is_accepted,
            author_id=current_user.get_id(),
            caption=form.caption.data,
            thumbnail=form.thumbnail.data)

        db.session.add(article)
        db.session.commit()

        flash('הפוסט נוצר בהצלחה וממתין לאישור מנהל.', 'success')

        return redirect(url_for('articles', index=article.article_id))

    return render_template('submitArticle.html',  form=form)

@app.route('/create-article/', methods=['GET', 'POST'])
@login_required
def createArticle():
    article = Article(
        heading='',
        body='',
        post_date=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        accept_date=None,
        is_accepted=False,
        author_id=current_user.get_id(),
        caption='',
        thumbnail='')

    db.session.add(article)
    db.session.commit()

    return redirect(url_for('editArticle', index=article.article_id))


@app.route('/control-panel')
@login_required
@admin_required
def controlPanel():
    inactiveUsers = User.get_all_inactive()
    inactiveArticles = Article.get_all_unaccepted()

    return render_template('controlPanel.html',  inactiveUsers = inactiveUsers, inactiveArticles = inactiveArticles)


"""
accept system stuff
"""
@app.route("/acceptuser/<index>", methods=['GET', 'POST'])
@login_required
@admin_required
def acceptUser(index):
    user = User.query.get(index)
    
    if user:
        user.accept_user()
    
    return redirect(url_for('controlPanel'))

@app.route("/deleteuser/<index>", methods=['GET', 'POST'])
@login_required
@admin_required
def deleteUser(index):
    user = User.query.get(index)

    if user:
        user.delete_user()

    return redirect(url_for('controlPanel'))

@app.route("/acceptarticle/<index>", methods=['GET', 'POST'])
@login_required
@admin_required
def acceptArticle(index):
    article = Article.query.get(index)

    if article:
        article.accept_article()

    return redirect(url_for('controlPanel'))

@app.route("/deletearticle/<index>", methods=['GET', 'POST'])
@login_required
@admin_required
def deleteArticle(index):
    article = Article.query.get(index)

    if article:
        article.delete_article()

    return redirect(url_for('controlPanel'))

@app.route('/article/<index>/')
def articles(index):
    article = Article.query.get(index)
    
    if not article:
        abort(404, description="Resource not found")
    
    elif not article.is_accepted:
        if not (current_user.is_authenticated and (current_user.user_id == article.author_id or current_user.is_admin())):
            abort(404, description="Resource not found")

    author = article.get_author()
    return render_template('articles.html', 
                         
                        article=article,
                        articleBody=md.render(article.body),
                        articleAuthor=f"{author.first_name} {author.last_name}, {author.school_class}")

@app.errorhandler(404)
def not_found(exc):
    return Response(render_template('404.html', title="Page Not Found")), 404