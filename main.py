#!/usr/bin/env python3
"""Flask app
Runs the flask app
"""

from flask import (
    Flask,
    render_template,
    request
)
from git_api import get_repo_details
from add import *

app = Flask(__name__)

app.debug = True


@app.route('/', strict_slashes=False)
def index():
    """Index
    """
    return render_template('index.html', title="Home")


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
