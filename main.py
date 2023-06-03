#!/usr/bin/env python3
"""Flask app
Runs the flask app
"""

from flask import (
    Flask,
    render_template,
    request,
    redirect,
)
from flask_login import (
    LoginManager,
    UserMixin,
    current_user
)
from git_api import *
from add import *
import os

app = Flask(__name__)
login_manager = LoginManager(app)

app.debug = True
app.secret_key = os.urandom(24)

# User class
class User(UserMixin):
    """User class
    """
    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

@login_manager.user_loader
def load_user(username):
    """Load user
    """
    user = User('achira', 'jacobachiraoabara')
    if user.username == username:
        return user

    return None

@app.route('/', strict_slashes=False)
def index():
    """Index
    """
    if request.args.get('code'):
        data = get_user_details(request.args.get('code'))
    else:
        data = "No data!"
    if current_user.is_authenticated:
        pass
    return render_template(
        'index.html',
        title="Home",
        data=data,
        code=request.args.get('code')
    )


@app.route('/test', strict_slashes=False)
def test():
    """Test
    """



    return render_template(
        'test.html',
        title="Test",
        code=request.args.get('code')
    )

# Generate authorization url
@app.route('/auth', strict_slashes=False)
def auth():
    """Auth
    """
    # redirect to authorization url
    return redirect(get_auth_url())


@app.route('/blogs', strict_slashes=False)
def blogs():
    """Blogs
    """
    return render_template('blogs.html', title="Blogs")


@app.route('/projects', strict_slashes=False)
@app.route('/projects/<name>', strict_slashes=False)
def projects(name={}):
    """Projects
    """
    if name:
        repo = get_repo_details(name)
        return render_template('projects.html', title="Project", repo=repo)

    return render_template('projects.html', title="Projects")


@app.route('/wellness', strict_slashes=False)
def wellness():
    """Wellness
    """
    return render_template('health_articles.html', title="Wellness")

@app.route('/register', strict_slashes=False, methods=['POST', 'GET'])
@app.route('/register/<name>', strict_slashes=False)
def register():
    """Register
    """
    if request.method == 'POST':
        details = {
            'name': request.form['name'],
            'username': request.form['username'],
            'gender': request.form['gender']
        }

        return render_template(
            'profile.html',
            title = 'Success',
            details=details
        )

    return render_template(
        'register.html',
        title="Register"
    )


@app.route('/about', strict_slashes=False)
def about():
    """About
    """

    return render_template('about.html', title="About")

@app.route('/contact', strict_slashes=False)
def contact():
    """Contact
    """

    return render_template('contact.html', title="Contact")

@app.route('/login', strict_slashes=False)
def login():
    """Login
    """

    return render_template('login.html', title="Login")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
