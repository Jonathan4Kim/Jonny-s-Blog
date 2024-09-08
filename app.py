from flask import Flask, request, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Flask constructor: creates flask instance
app = Flask(__name__)
# connects app to the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# encrypt data by giving a secret key
app.config['SECRET_KEY'] = 'aoitodo'
# creates database
db = SQLAlchemy(app=app)


# create user database
class User(db.Model, UserMixin):
    """
    SQLAlchemy User class.
    Attributes:
        1. id: user_id (private)
        2. email: their username
        3. password: their passoword
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


class Articles(db.Model):
    """
    SQLAlchemy Articles class.
    Attributes:
        1. article_id: unique and hashed
        2. id: id of user who wrote the article
        3. title: title of article
        4. html content of the article
    """
    article_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer)
    title = db.Column(db.String(150), nullable=False, unique=True)
    article = db.Column(db.String(30000), nullable=False)


# Route for displaying the form, home page
@app.route('/')
def home():
    # just return html home: routing will come from nav bar in file
    return render_template('home.html')


@app.route('/create', methods=["GET", "POST"])
def create():
    if session['user_id']:
        # create article html template
        return render_template('create_article.html')
    return redirect(url_for('create'))


@app.route('/login',  methods=["GET", "POST"])
def login():
    # first, check for a post request method (it's a form)
    if request.method == "POST":

        # get the email and password from requests
        email = request.form.get('email')
        password = request.form.get('password')

        # search for an existing user 
        existing_user = User.query.filter_by(email=email, password=password).first()

        # if the user exists
        if existing_user:
            print("saving session into id...")

            # create a new session with the user id
            session['user_id'] = existing_user.id
            return redirect(url_for('create'))
        # if not, throw an error here

    # if we haven't found an existing user, render the login screen again.
    return render_template('login.html')


@app.route('/register',  methods=["GET", "POST"])
def register():

    # again, this is a form, so make sure method is post
    if request.method == "POST":

        # get the email and password from requests, and the confirmed password as well
        email = request.form.get("email")
        password = request.form.get("password")
        confirmed_password = request.form.get("confirm-password")

        # if passwords dont match, throw an error and return to register
        if confirmed_password != password:
            print("here unconfirmed password")
            flash('There is an error in your password confirmation. Please make sure the passwords are the same')
            return render_template('register.html')

        # otherwise, create a new user and add to sql databas
        new_user = User(id=create_unique_id(email), email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        # redirect to the login page to login to their new account
        return redirect(url_for('login'))

    # otherwise register
    return render_template('register.html')


@app.route('/submit', methods=["POST"])
def submit():

    # get the article title from the form
    title = request.form.get("art_title")

    # if the title already exists, throw an error
    if Articles.query.filter_by(title=title).first():
        error = "Error:Title already exists"
        print('here')
        return render_template('create_article.html', error=error)

    # get the article content
    article = request.form.get("article-content")

    # create a new article and add it to the db
    new_article = Articles(article_id=create_unique_id(title), id=session['user_id'], title=title, article=article)
    db.session.add(new_article)
    db.session.commit()

    # redirect the page to all the past articles
    return redirect(url_for("see_past_articles"))


@app.route('/signout', methods=["GET", "POST"])
def sign_out():

    # clear session user id
    session['user_id'] = None

    # redirect to home
    return redirect(url_for('home'))


@app.route('/past_articles', methods=["GET"])
def see_past_articles():
    # get all articles from a user_id perspective
    all_articles = Articles.query.filter_by(id=session['user_id'])
    # load them into an html file
    return render_template('all_articles.html', articles=all_articles)


@app.route('/see-article/<article_name>', methods=["GET", "POST"])
def see_article(article_name):

    # get the article information from articles class db
    article = Articles.query.filter_by(id=session['user_id'],
                                       title=article_name).first()

    # pass it to the display article
    return render_template('display_article.html', article=article)


@app.route('/edit_article', methods=["GET", "POST"])
def edit_article():
    # get the article title and content
    article_title = request.form.get('art_title')
    article_content = request.form.get('article-content')

    # pass it to the edit article template, similar to create, but initialized with article content in each field
    return render_template('edit_article.html',
                           article_title=article_title,
                           article_content=article_content)

@app.route('/submit_edit', methods=["POST"])
def submit_edit():
    # get the article title from the form
    title = request.form.get("old_art_title")

    # get the instance
    instance = Articles.query.filter_by(title=title).first()

    # get the article title and content, and set them to new values
    instance.title = request.form.get("art_title")
    instance.article = request.form.get('article-content')

    # commit changes and return to all articles
    db.session.commit()
    return render_template('all_articles.html')


def create_unique_id(email):
    # helper function: hash user id
    return abs(hash(email))


if __name__ == '__main__':
    app.run(debug=True)
    with app.app_context():
        db.create_all()
