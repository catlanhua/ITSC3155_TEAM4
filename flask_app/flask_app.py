# FLASK Tutorial 1 -- We show the bare bones code to get an app up and running

# imports
import os                 # os is used to get environment variables IP & PORT
from flask import Flask   # Flask is the web app that we will customize
from flask import render_template
from flask import request
from flask import redirect, url_for, session
from database import db
from models import Post as Post
from models import User as User
from forms import RegisterForm
import bcrypt

app = Flask(__name__)     # create an app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_qna_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['SECRET_KEY'] = 'SE3155'
#  Bind SQLAlchemy db object to this Flask app
db.init_app(app)
# Setup models
with app.app_context():
    db.create_all()   # run under the app context

# @app.route is a decorator. It gives the function "index" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page


@app.route('/')
@app.route('/index')
def index():
    a_user = db.session.query(User).filter_by(email='chua@uncc.edu').one()
    return render_template('index.html', user=a_user)


@app.route('/posts')
def get_posts():
    if session.get('user'):
        my_posts = db.session.query(Post).filter_by(user_id=session['user_id']).all()
        return render_template('posts.html', posts=my_posts, user=session['user'])
    else:
        return redirect(url_for('login'))


@app.route('/posts/<post_id>')
def get_post(post_id):
    a_user = db.session.query(User).filter_by(email='chua@uncc.edu').one()
    my_post = db.session.query(Post).filter_by(id=post_id).one()
    return render_template('post.html', post=my_post, user=a_user)


@app.route('/posts/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['postText']
        from datetime import date
        today = date.today()
        today = today.strftime("%m-%d-%Y")
        new_record = Post(title, text, today)
        db.session.add(new_record)
        db.session.commit()

        return redirect(url_for('get_posts'))
    else:
        a_user = db.session.query(User).filter_by(email='chua@uncc.edu').one()
        return render_template('new.html', user=a_user)

@app.route('/posts/edit/<post_id>', methods=['GET', 'POST'])
def update_post(post_id):
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['postText']
        my_post = db.session.query(Post).filter_by(id=post_id).one()
        # update note data
        my_post.title = title
        my_post.text = text
        # update note in db
        db.session.add(my_post)
        db.session.commit()
        return redirect(url_for('get_posts'))
    else:
        a_user = db.session.query(User).filter_by(email='chua@uncc.edu').one()
        my_post = db.session.query(Post).filter_by(id=post_id).one()
        return render_template('new.html', post=my_post, user=a_user)

@app.route('/posts/delete/<post_id>', methods=['POST'])
def delete_post(post_id):
    # retrieve note from database
    my_post = db.session.query(Post).filter_by(id=post_id).one()
    db.session.delete(my_post)
    db.session.commit()

    return redirect(url_for('get_posts'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()

    if request.method == 'POST' and form.validate_on_submit():
        # salt and hash password
        h_password = bcrypt.hashpw(
            request.form['password'].encode('utf-8'), bcrypt.gensalt())
        # get entered user data
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        # create user model
        new_user = User(first_name, last_name, request.form['email'], h_password)
        # add user to database and commit
        db.session.add(new_user)
        db.session.commit()
        # save the user's name to the session
        session['user'] = first_name
        session['user_id'] = new_user.id  # access id value from user model of this newly added user
        # show user dashboard view
        return redirect(url_for('get_posts'))

    # something went wrong - display register view
    return render_template('register.html', form=form)
app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)),debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.

