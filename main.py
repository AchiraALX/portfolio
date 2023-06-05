#!/usr/bin/env python3
"""Flask app
Runs the flask app
"""

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    url_for
)
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user
)
from git_api import *
from add import *
import os
from queries import *
from add import Add
add = Add()

app = Flask(__name__)
login_manager = LoginManager(app)

app.debug = True
app.secret_key = os.urandom(24)
login_manager.init_app(app)
message = None

class User(UserMixin):
    """User
    """
    global query_user

    def __init__(self, username):
        self.username = username
        self.user = query_user(self.username)

    def get_id(self):
        """Get id
        """
        return self.username

    def __repr__(self):
        return f'<User: {self.username}>'

@login_manager.user_loader
def load_user(username):
    """Load user
    """
    return User(username)

@app.route('/', strict_slashes=False)
def index():
    """Index
    """

    if request.args.get('code'):
        data = get_user_details(request.args.get('code'))
        if 'login' in data:
            pass
    else:
        data = "No data!"

    if current_user.is_authenticated:
        user = current_user.username
    else:
        user = 'Guest'

    return render_template(
        'index.html',
        title="Home",
        data=data,
        code=request.args.get('code'),
        user=user
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
    data = main('blogs')['blogs']
    return render_template('blogs.html', title="Blogs", blogs=data)


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

    data = main('heats')['heats']
    return render_template('health_articles.html', title="Wellness", data=data)


@login_required
@app.route('/tasks', strict_slashes=False)
def tasks():
    """Tasks
    """
    all_tasks = main('tasks')['tasks']
    tasks = []
    for task in all_tasks:
        if task['assigneeId'] == current_user.user['id']:
            tasks.append(task)

    print(tasks)

    return render_template('tasks.html', title="Tasks", tasks=tasks, date=datetime.utcnow())


@app.route('/register', strict_slashes=False, methods=['POST', 'GET'])
@app.route('/register/<name>', strict_slashes=False)
def register():
    """Register
    """
    if request.method == 'POST':
        add = Add()
        details = {
            'username': request.form['username'],
            'password': request.form['password'],
            'email': request.form['email'],
            'gender': request.form['gender'],
            'name': request.form['name']
        }

        if query_user(details['username']):
            flash("User already exists")
            return redirect(url_for('register'))

        try:
            add.add_user(**details)
            flash("User seem to have been added successfully")
            return redirect(url_for('login'))
        except Exception as e:
            flash("Error adding user")
            return redirect(url_for('register'))

        else:
            flash('Fatal error', 'warning')
            return

    return render_template('register.html', title="Register")


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


@app.route('/login', strict_slashes=False, methods=['POST', 'GET'])
def login():
    """Login
    """
    message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = query_user(username)

        if user:
            if user['password'] == password and user['username'] == username:
                login_user(User(username))
                flash('You were successfully logged in')
                return redirect('/profile')
            elif user['password'] != password:
                message = 'Invalid password'

            elif user['username'] != username:
                message = 'Invalid username'

            else:
                message = 'Invalid credentials'
        else:
            flash("User doesn't exist")
            return redirect('/register')

    return render_template('login.html', title="Login", message=message)


@app.route('/logout', strict_slashes=False)
def logout():
    """Logout
    """
    logout_user()
    return redirect('/')

@login_required
@app.route('/profile', strict_slashes=False)
def profile():
    """Profile
    """

    return render_template('profile.html', title="Profile")


@app.route('/index_heat_and_blog', strict_slashes=False)
@app.route('/index_heat_and_blog/<num>', strict_slashes=False)
def two_articles(num=2):
    """Return data that will be rendered on home page"""
    try:
        num = int(num)
        if request.args.get('num'):
            num = int(request.args.get('num'))

    except ValueError:
        return redirect(url_for('index_heat_and_blog'))


    heats = main('heats')['heats'][:num]
    blogs = main('blogs')['blogs'][:num]

    data = {
        'blogs': blogs,
        'heats': heats
    }

    return dict(data)


# Single article
@app.route('/blog/<id>', strict_slashes=False)
def blog(id):
    """Blog
    """
    try:
        id = int(id)
    except ValueError:
        return redirect(url_for('blogs'))

    blog = get_blog(id)
    return render_template('blog.html', title=blog['blogTitle'], blog=blog)

@app.route('/article', strict_slashes=False)
@app.route('/article/<id>', strict_slashes=False)
def article(id):
    """Wellness article
    """

    try:
        id = int(id)
        if request.args.get('id'):
            id = int(request.args.get('id'))

    except ValueError:
        flash("Broken URL. Redirected to blogs")
        return redirect(url_for('wellness'))

    article = get_article(id)
    print(article)
    return render_template('article.html', title=article['title'], article=article)

# Deal with messages
def get_message_and_category(
    text: str,
    category: str = 'info') -> dict:
    """Format to render message

    Args:
        message (str): the message
        category (str): category it belongs

    Returns:
        dict: dictionary
    """
    return {
        'text': text,
        'category': category
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
