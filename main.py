#!/usr/bin/env python3
"""Flask app
Runs the flask app
"""

import contextlib
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    url_for,
    abort
)
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user
)
from funcs import get_task_status
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
        try:
            data = get_user_details(request.args.get('code'))
            username = data['login']
            password = str(data['id']) + data['login']
            email = data['login'] + '@gmail.com'
            gender = 'o'
            name = data['name']

            details = {
                'username': username,
                'password': password,
                'email': email,
                'name': name,
                'gender': gender
            }

            user = query_user(username)

            if user:
                log_user_in(user, password, username)
            else:
                sign_up(**details)
        except Exception as e:
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

# Login with auth
@app.route('/auth_login', strict_slashes=False)
def auth_login():
    """Auth login
    """
    # redirect to authorization url
    return redirect(get_auth_url())

@app.route('/blogs', strict_slashes=False, methods=['GET', 'POST'])
def blogs():
    """Blogs
    """
    if request.method == 'POST':
        if current_user.is_authenticated:
            add = Add()
            blog_title = request.form['title']
            blog_content = request.form['content']
            author = current_user.username

            details = {
                'blog_title': blog_title,
                'blog_content': blog_content,
                'author': author
            }

            failed = []
            for key, value in details.items():
                if not value:
                    failed.append(key)

            if len(failed) > 0:
                flash(f"Some values failed. {failed!r}")
                return redirect(url_for('blogs'))

            try:
                add.add_blog(**details)
            except Exception as e:
                flash(f"Error {e!r} redirected")
                return redirect(url_for('blogs'))

        else:
            flash('Log in first')
            return redirect(url_for('login'))
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


@app.route('/wellness', strict_slashes=False, methods=['POST', 'GET'])
def wellness():
    """Wellness
    """

    if request.method == 'POST':
        if current_user.is_authenticated:
            title = request.form['title']
            content = request.form['content']
            author = current_user.username

            details = {
                'title': title,
                'content': content,
                'author': author
            }

            failed = []
            for key, value in details.items():
                if not value:
                    failed.append(key)

            if len(failed) >  0:
                flash(f"Some values are failing {failed!r}")

            add = Add()

            try:
                add.add_heat(**details)

            except Exception as e:
                flash("Error {e!r}")

            return redirect(url_for('wellness'))

        else:
            flash("Login first.")

    data = main('heats')['heats']
    return render_template('health_articles.html', title="Wellness", data=data)


@login_required
@app.route('/tasks', strict_slashes=False, methods=['POST', 'GET'])
def tasks(id=None):
    """Tasks
    """
    if current_user.is_authenticated:
        if request.method == 'POST':
            task_title = request.form['title']
            task_description = request.form['content']
            task_assignee = current_user.username
            task_status = 'pending'

            details = {
                'task_title': task_title,
                'task_description': task_description,
                'task_assignee': task_assignee,
                'task_status': task_status
            }

            failed = []
            for key, value in details.items():
                if not value:
                    failed.append(key)

            if len(failed) > 0:
                flash(f"Some values failed {failed!r}")
                return redirect(url_for('tasks'))

            add = Add()
            try:
                add.add_task(**details)

            except Exception as e:
                flash("Error {e!r}")

            return redirect(url_for('tasks'))

        all_tasks = main('tasks')['tasks']
        yellow_tasks = []
        red_tasks = []
        blue_tasks = []
        green_task = []

        for task in all_tasks:
            if task['assigneeId'] == current_user.user['id']:
                status = get_task_status(task['taskDueDate'])
                match status:
                    case 'Past Due':
                        red_tasks.append(task)

                    case 'In Progress':
                        yellow_tasks.append(task)

                    case 'Future Task':
                        blue_tasks.append(task)
                if task['taskStatus'] != 'pending':
                    green_task.append(task)
        print(tasks)

        return render_template(
            'tasks.html',
            title="Tasks",
            y_t=yellow_tasks,
            r_t=red_tasks,
            b_t=blue_tasks
        )

    flash("Login to access tasks!")
    return redirect(url_for('login'))


@app.route('/register', strict_slashes=False, methods=['POST', 'GET'])
@app.route('/register/<name>', strict_slashes=False)
def register():
    """Register
    """
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        gender = request.form['gender']

        details = {
            'name': name,
            'username': username,
            'password': password,
            'email': email,
            'gender': gender
        }
        failed = []
        for key, value in details.items():
            if not value:
                failed.append(key)

        if len(failed) > 0:
            flash(f"Some values failed. {failed!r}")
            return redirect(url_for('register'))

        return sign_up(**details)

    return render_template('register.html', title="Register")

# Sign up
def sign_up(name, username, password, email, gender):
    add = Add()
    details = {
        'username': username,
        'password': password,
        'email': email,
        'gender': gender,
        'name': name
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
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = query_user(username)

        return log_user_in(user, password, username)

    return render_template('login.html', title="Login")


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

    if current_user.is_authenticated:
        return render_template(
            'profile.html',
            title=current_user.user['name']
        )

    else:
        flash("Login to view profile")
        return redirect(url_for('login'))

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

# Get all repository details and ghubs
@app.route('/ghub_repos', strict_slashes=False)
@app.route('/ghub_repos/<num>', strict_slashes=False)
def ghubs_repos(num=3):
    """Return ghubs and repos for the user"""
    if current_user.is_authenticated:
        try:
            num = int(num)
            if request.args.get('num'):
                num = int(request.args.get('num'))

        except ValueError:
            return redirect(url_for('profile'))

        repos = get_repos(current_user.user['id'])[:num]
        ghubs = get_ghub(current_user.user['id'])[:num]

        data = {
            'repos': repos,
            'ghubs': ghubs
        }

        return dict(data)

    flash("Login to view repos and ghub")
    return redirect(url_for('login'))


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
    return render_template('article.html', title=article['title'], article=article)


# Route for single article
@app.route('/task/<id>', strict_slashes=False)
def one_task(id):
    """Get a single task

    Args:
        id (_type_, optional): _description_. Defaults to None.
    """

    if current_user.is_authenticated:
        print("Passed")
        try:
            id = int(id)
            if request.args.get('id'):
                id = int(request.args.get('id'))

        except ValueError:
            flash("Broken URL. Aborted")
            abort(404)

        task = get_task(id)
        if task['assigneeId'] == current_user.user['id']:
            return render_template(
                'task.html',
                title=get_task_status(task['taskDueDate']),
                task=task
            )
        else:
            abort(404)

    flash("Login to access the task")
    return redirect(url_for('login'))


# Route for blog comments
@app.route('/blog_comments', strict_slashes=False, methods=['POST', 'GET'])
def blog_comments():
    """Load blog comment as per blog
    """

    if current_user.is_authenticated:
        if request.method == 'POST':
            comment = request.form['comment']
            author = current_user.username
            try:
                blog_id = request.args.get('blog_id')
            except Exception as e:
                flash("Can't resolve the blog.")
                return redirect(url_for('blogs'))

            details = {
                'comment': comment,
                'author': author,
                'blog_id': blog_id
            }

            failed = []
            for key, value in details.items():
                if not value:
                    failed.append(key)

            if len(failed) > 0:
                flash("Some values failed {failed!r}")
                return redirect(url_for('blogs'))

            add = Add()

            try:
                add.add_blog_comment(**details)
            except Exception as e:
                flash(f"Error {e!r}")
                return redirect(url_for('blogs'))

    if request.args.get('id'):
        id = request.args.get('id')
        try:
            id = int(id)
        except Exception as e:
            flash("Error while loading comments")
            return redirect(url_for('blogs'))

        available_comment = get_blog_comments(id)

        return available_comment
    else:
        flash("Can't get comments")
        return redirect(url_for('blogs'))

@app.errorhandler(404)
def handle_not_found(error):
    """Handle 404
    """

    return render_template('404.html', title="404")

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

# Login user
def log_user_in(user, password, username):
    if user:
        if user['password'] == password and user['username'] == username:
            login_user(User(username))
            flash('You were successfully logged in')
            return redirect('/profile')
        elif user['password'] != password:
            flash('Invalid password')

        elif user['username'] != username:
            flash('Invalid username')

        else:
            flash('Invalid username and password')
    else:
        flash("User doesn't exist")
        return redirect('/register')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
