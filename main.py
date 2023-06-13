#!/usr/bin/env python3
"""Flask app
Runs the flask app
"""

from delete import Delete
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
from flask_cors import CORS
from git_api import *
from add import *
import os
from queries import *
from add import Add
add = Add()

app = Flask(__name__)
login_manager = LoginManager(app)

app.debug = False
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
CORS(app, resources={r"/*": {"origins": "*"}})
app.secret_key = os.urandom(24)
login_manager.init_app(app)
message = None

class User(UserMixin):
    """Control logged in sessions
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
    """Return a session with a user logged in
    instantiated by the UserMixin in User class
    """
    return User(username)

@app.route('/', strict_slashes=False)
def index():
    """The index route, the home page route
    """

    if request.args.get('code'):
        """Handle the callback from GitHub
        If user exists, log them in
        If user does not exist, sign them up
        """
        try:
            """Get the username, name, and id from GitHub
            Set gender to 'o' for other
            make a generic password using the id and username
            make a generic email using the username
            """
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

            flash(data)

            user = query_user(username)

            if user:
                print('User exists login')
                log_user_in(user, password, username)
            else:
                print('User does not exist sign up')
                sign_up(**details)
        except Exception as e:
            pass

    else:
        data = "No data!"

    # If the user is logged in, get their username
    # If the user is not logged in, set the username to Guest
    if current_user.is_authenticated:
        user = current_user.username
    else:
        user = 'Guest'

    # Render the index.html template
    # Pass the data, title, and user to the template
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


# Define the blogs route
@app.route('/blogs', strict_slashes=False, methods=['GET', 'POST'])
def blogs():
    """Render blogs using the blogs.html template
    """
    if request.method == 'POST':
        # If a request is POST save try to save the blog
        # for failed values, flash a message and redirect back
        # for successful values, add the blog to the database
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

    # Get the blogs from the database
    # Sort the blogs by date
    # Render the blogs.html template
    data = main('blogs')['blogs']
    data = sorted(data, key=lambda x: x['blogPublishedDate'], reverse=True)
    return render_template('blogs.html', title="Blogs", blogs=data)


# Define the projects route and
# the projects/<name> route
@app.route('/projects', strict_slashes=False, methods=['GET', 'POST'])
@app.route('/projects/<name>', strict_slashes=False, methods=['GET', 'POST'])
def projects(name=None):
    """Render all projects using the projects.html template
    For the projects/<name> route, render a single detailed project
    """

    # Set token to None an try accessing token from the current user
    # Pass if the token is not available
    token = None
    with contextlib.suppress(Exception):
        token = current_user.user['tokens'][0]['token']

    if current_user.is_authenticated:
        if request.args.get('name') or name:
            if request.args.get('name'):
                name = request.args.get('name')
            if name:
                name = name

            token = None
            # Try checking the token from the current user
            # If it fails, check the token from the database
            # If it fails, redirect to the referrer
            try:
                token = current_user.user['tokens'][0]['token']
                if not token:
                    token = query_user(current_user.username)['tokens'][0]['token']

            except Exception as e:
                flash(f"Error {e!r} redirected")
                return redirect(request.referrer)

            # Fetch the GitHub username using the GitHub token
            # and get the repository details
            username = get_username(token)
            repo = get_repo_details(token, name, username)
            if 'error' in repo:
                flash(repo['error'])
                return redirect(request.referrer)

            return render_template('projects.html', title="Project", repo=repo)

        # Set the repos to None and query the current user
        # get available_repos from the already saved repos in the database
        repos = None
        user = query_user(current_user.username)
        available_repos = get_user_repos(current_user.user['id'])
        if request.method == 'POST':
            # For POST requests, get the data from the form
            # If saving is set to 'y', save the token to the database
            # Else use the token to query repos from github
            # and discard the token
            user = user
            token = request.form['token']
            saving = request.form['save']


            details = {
                'token': token,
                'user_info': user
            }

            failed = []
            for key, value in details.items():
                if not value:
                    failed.append(key)

            if len(failed) > 0:
                # Redirect if their are value that are empty
                flash(f"Some values failed. {failed!r}")

            else:
                # Try get the repos from GitHub using the token
                # and report any errors
                repos = git_all_repos(token)
                if 'error' in repos:
                    flash(repos['error'])
                    return redirect(url_for('projects'))

                if saving == 'y':
                    if not get_user_tokens(current_user.username, token):
                        add = Add()
                        user = add.get_user(current_user.username)
                        token = {
                            'token': token,
                            'user_info': user
                        }
                        add.add_token(**token)

                # Render the projects.html template
                # Pass the repos concatenating the available_repos
                return render_template(
                    'projects.html',
                    title="Projects",
                    repos=repos + available_repos,
                )
        # Special repo is the repo that is displayed on the
        # user profile in github
        special = None
        if token:
            try:
                available_repos = git_all_repos(token) + available_repos
                special = get_special_repo(token)

            except Exception as e:
                flash(f"Error {e!r}")
                return redirect(request.referrer)

        # Render the projects.html template
        # Pass the available_repos and special
        return render_template(
            'projects.html',
            title="Projects",
            repos=available_repos,
            special=special
        )

    return render_template('projects.html', title="Projects")


# Define the wellness route
@app.route('/wellness', strict_slashes=False, methods=['POST', 'GET'])
def wellness():
    """Render the wellness.html template
    Routes to the wellness dashboard
    """

    if request.method == 'POST':
        # If the request method is POST
        # Extract the data from the form
        # If the user is authenticated,
        # get the username and try
        # saving the article with the username as the author
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
                flash(f"Error {e!r}")

            return redirect(url_for('wellness'))

        else:
            flash("Login first.")

    # Get health articles from the database
    # Sort the articles by the published date
    # and render the wellness.html template
    data = main('heats')['heats']
    data = sorted(data, key=lambda x: x['publishedDate'], reverse=True)
    return render_template('health_articles.html', title="Wellness", data=data)


# Define the tasks route
@login_required
@app.route('/tasks', strict_slashes=False, methods=['POST', 'GET'])
def tasks(id=None):
    """Routes to the user tasks dashboard
    """

    # If the user is authenticated and the request method is POST
    # Extract the data from the form
    # If the data is not empty, try adding the task to the database
    # Else redirect to the tasks dashboard
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

        # Get all the tasks from the database
        # Sort the tasks by the due date
        # and render the tasks.html template
        all_tasks = main('tasks')['tasks']
        yellow_tasks = []
        red_tasks = []
        blue_tasks = []
        green_task = []

        for task in all_tasks:
            if task['assigneeId'] == current_user.user['id']:
                status = get_task_status(task['taskDueDate'])
                if status == 'Past Due':
                    red_tasks.append(task)

                elif status == 'In Progress':
                    yellow_tasks.append(task)

                else:
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


# Define the register route
@app.route('/register', strict_slashes=False, methods=['POST', 'GET'])
@app.route('/register/<name>', strict_slashes=False)
def register():
    """Routes to the register page
    """

    # If the request method is POST
    # Extract the data from the form
    # If the data is not empty, try signing up the user
    # Else redirect to the register page

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
def sign_up(
    name: str,
    username: str,
    password: str,
    email: str,
    gender: str
) -> None:
    """Saves a user into the database

    Arguments:
        name {str} -- Name of the user
        username {str} -- Username of the user
        password {str} -- Password of the user
        email {str} -- Email of the user
        gender {str} -- Gender of the user
    """
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

    # Try saving the user to the database
    # If it fails, redirect to register
    try:
        add.add_user(**details)
        flash("User seem to have been added successfully")
        return redirect(url_for('login'))
    except Exception as e:
        flash("Error adding user")
        return redirect(url_for('register'))


# Define the about route
@app.route('/about', strict_slashes=False)
def about():
    """Routes to the about page
    """

    return render_template('about.html', title="About")


# Define the contact route
@app.route('/contact', strict_slashes=False)
def contact():
    """Routes to the contact page
    """

    return render_template('contact.html', title="Contact")


# Define the login route
@app.route('/login', strict_slashes=False, methods=['POST', 'GET'])
def login():
    """Routes to the login page
    """

    # If the request method is POST
    # Extract the data from the form
    # If the data is not empty, try logging in the user
    # Else redirect to the login page
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = query_user(username)

        return log_user_in(user, password, username)

    return render_template('login.html', title="Login")


# Define the logout route
@app.route('/logout', strict_slashes=False)
def logout():
    """Logout user out of the system
    """
    logout_user()
    return redirect('/')


# Define the profile route
@login_required
@app.route('/profile', strict_slashes=False)
def profile():
    """Routes to the profile page
    """

    # If the user is logged in
    # Render the profile page
    if current_user.is_authenticated:
        return render_template(
            'profile.html',
            title=current_user.user['name']
        )

    else:
        flash("Login to view profile")
        return redirect(url_for('login'))


# Define the health and blogs
# available on the home page
# endpoints
@app.route('/index_heat_and_blog', strict_slashes=False)
@app.route('/index_heat_and_blog/<num>', strict_slashes=False)
def two_articles(num=2):
    """Return data that will be rendered on home page

    Arguments:
        num {int} -- Number of articles to return
    """
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
    """Return ghubs and repos for the user

    Arguments:
        num {int} -- Number of repos and ghubs to return
    """
    if current_user.is_authenticated:
        try:
            num = int(num)
            if request.args.get('num'):
                num = int(request.args.get('num'))

        except ValueError:
            return redirect(url_for('profile'))

        repos = get_user_repos(current_user.user['id'])[:num]
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
    """Return a single blog page

    Arguments:
        id {int} -- Id of the blog
    """
    try:
        id = int(id)
    except ValueError:
        return redirect(url_for('blogs'))

    blog = get_blog(id)
    return render_template('blog.html', title=blog['blogTitle'], blog=blog)


@app.route('/article/<id>', strict_slashes=False)
def article(id):
    """Return a single article page

    Arguments:
        id {int} -- Id of the article
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
    """Return a single task page

    Arguments:
        id {int} -- Id of the task
    """

    if current_user.is_authenticated:
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

    if request.method == 'POST':
        if current_user.is_authenticated:
            comment = request.form['comment']
            blog = request.form['blog']
            author = current_user.username

            details = {
                'comment': comment,
                'blog': blog,
                'author': author
            }

            failed = []
            for key, value in details.items():
                if not value:
                    failed.append(key)

            if failed:
                flash(f"Fill in the required fields{failed!r}")
                return redirect(request.referrer)

            add = Add()
            try:
                add.add_blog_comment(**details)
                flash("Comment added")
                return redirect(request.referrer)
            except Exception as e:
                flash("Error while adding comment")
                return redirect(request.referrer)
        else:
            flash("Login to comment")
            return redirect(url_for('login'))

    if request.args.get('id'):
        id = request.args.get('id')
        try:
            id = int(id)
        except Exception as e:
            flash("Error while loading comments")
            return redirect(url_for('blogs'))

        available_comment = get_blog_comments(id)
        available_comment.sort(key=lambda x: x['commentDate'], reverse=True)
        return available_comment

    return redirect(url_for('blogs'))


# Route to handle the health article comments
@app.route('/article_comments', strict_slashes=False, methods=['POST', 'GET'])
def article_comments():
    """Load article comment as per article
    """

    if request.method == 'POST':
        if current_user.is_authenticated:
            comment = request.form['comment']
            print(comment)
            heat = request.form['article']
            print(heat)
            author = current_user.username
            print(author)

            details = {
                'comment': comment,
                'heat': heat,
                'author': author
            }

            failed = []
            for key, value in details.items():
                if not value:
                    failed.append(key)

            if failed:
                flash(f"Fill in the required fields{failed!r}")
                return redirect(request.referrer)

            add = Add()
            try:
                add.add_heat_comment(**details)
                flash("Comment added")
                return redirect(request.referrer)
            except Exception as e:
                flash("Error while adding comment")
                return redirect(request.referrer)
        else:
            flash("Login to comment")
            return redirect(url_for('login'))

    if request.args.get('id'):
        id = request.args.get('id')
        try:
            id = int(id)
        except Exception as e:
            flash("Error while loading comments")
            return redirect(url_for('wellness'))

        available_comment = get_article_comments(id)
        return available_comment

    return redirect(url_for('wellness'))

@app.errorhandler(404)
def handle_not_found(error):
    """Handle 404
    """

    return render_template('404.html', title="404")

@app.errorhandler(400)
def handle_bad_request(error):
    """Handle 400
    """

    return render_template('400.html', title="400", error=error)

# Delete a user
@app.route('/delete_user', strict_slashes=False, methods=['POST', 'GET'])
def delete_user():
    """Delete a user
    """
    if not request.args.get('username'):
        flash("No specified user")
        if not is_logged_in():
            return redirect(url_for('login'))
        return redirect(url_for('index'))

    if request.args.get('username'):
        if current_user.is_authenticated:
            user = query_user(current_user.username)
            if user['id'] == current_user.user['id']:
                delete = Delete()
                try:
                    delete.delete_user(user['id'])
                    flash("User deleted")
                    return redirect(url_for('logout'))
                except Exception as e:
                    flash("Error while deleting user")
                    return redirect(url_for('index'))
            else:
                flash("You can only delete your account")
                return redirect(url_for('index'))
        else:
            flash("Login to delete your account")
            return redirect(url_for('login'))

    return redirect(url_for('logout'))


# Delete a task if the ownerId is the current user
@app.route('/delete_task', strict_slashes=False, methods=['POST', 'GET'])
def delete_task():
    """Deletes a task if the ownerId is the current user
    """
    if request.args.get('id'):
        try:
            id = int(request.args.get('id'))
        except ValueError:
            flash("Bad argument")
            abort(400)

        if current_user.is_authenticated:
            try:
                task = get_task(int(id))
            except ValueError:
                flash("Broken URL. Aborted")
                abort(404)

            if task['assigneeId'] == current_user.user['id']:
                delete = Delete()
                try:
                    delete.delete_task(int(id))
                    flash("Task deleted")
                    return redirect(url_for('tasks'))
                except Exception as e:
                    flash("Error while deleting task")
                    return redirect(url_for('tasks'))
            else:
                flash("You are not authorized to perform this action")
                return redirect(url_for('tasks'))
        else:
            flash("Login to delete task")
            return redirect(url_for('login'))

    else:
        flash("No task specified")

    return redirect(url_for('tasks'))


# Delete a blog if the ownerId is the current user
@app.route('/delete_blog', strict_slashes=False, methods=['POST', 'GET'])
def delete_blog():
    """Deletes a blog if the ownerId is the current user
    """
    if request.args.get('id'):
        try:
            id = int(request.args.get('id'))
        except ValueError:
            flash("Bad argument")
            abort(400)

        if current_user.is_authenticated:
            try:
                blog = get_blog(id)
            except ValueError:
                flash("Broken URL. Aborted")
                abort(404)

            if blog['authorId'] == current_user.user['id']:
                delete = Delete()
                try:
                    delete.delete_blog(id)
                    flash("Blog deleted")
                    return redirect(url_for('blogs'))
                except Exception as e:
                    flash("Error while deleting blog")
                    return redirect(url_for('blogs'))
            else:
                flash("You are not authorized to perform this action")
                return redirect(url_for('blogs'))
        else:
            flash("Login to delete blog")
            return redirect(url_for('login'))
    else:
        flash("No blog specified")

    return redirect(url_for('blogs'))


# Delete a heat if the ownerId is the current user
@app.route('/delete_heat', strict_slashes=False, methods=['POST', 'GET'])
def delete_heat():
    """Deletes a heat if the ownerId is the current user
    """
    if request.args.get('id'):
        try:
            id = int(request.args.get('id'))
        except ValueError:
            flash("Bad argument")
            abort(400)

        if current_user.is_authenticated:
            try:
                heat = get_article(int(id))
            except ValueError:
                flash("Broken URL. Aborted")
                abort(404)

            if heat['ownerId'] == current_user.user['id']:
                delete = Delete()
                try:
                    delete.delete_heat(int(id))
                    flash("Heat deleted")
                    return redirect(url_for('wellness'))
                except Exception as e:
                    flash("Error while deleting heat")
                    return redirect(url_for('heats'))
            else:
                flash("You are not authorized to perform this action")
                return redirect(url_for('wellness'))
        else:
            flash("Login to delete heat")
            return redirect(url_for('login'))

    return redirect(url_for('wellness'))


# Delete a comment if the ownerId is the current user
@app.route('/delete_blog_comment', strict_slashes=False, methods=['POST', 'GET'])
def delete_comment():
    """Deletes a comment if the ownerId is the current user
    """
    if request.args.get('id'):
        try:
            id = int(request.args.get('id'))
        except ValueError:
            flash("Bad argument")
            abort(400)

        if current_user.is_authenticated:
            try:
                comment = get_blog_comment(int(id))

            except Exception as e:
                flash("Broken URL. Aborted")
                abort(404)

            if comment['authorId'] == current_user.user['id']:
                delete = Delete()
                try:
                    delete.delete_blog_comment(int(id))
                    flash("Comment deleted")
                    return redirect(url_for('blogs'))
                except Exception as e:
                    flash("Error while deleting comment")
                    return redirect(url_for('blogs'))
            else:
                flash("You are not authorized to perform this action")
                return redirect(url_for('blogs'))
        else:
            flash("Login to delete comment")
            return redirect(url_for('login'))

    return redirect(url_for('blogs'))


# Delete a task comment if the authorId is the current user
@app.route('/delete_task_comment', strict_slashes=False, methods=['POST', 'GET'])
def delete_task_comment():
    """Deletes a task comment if the authorId is the current user
    """
    if request.args.get('id'):
        try:
            id = int(request.args.get('id'))
        except ValueError:
            flash("Bad argument")
            abort(400)

        if current_user.is_authenticated:
            try:
                comment = get_task_comment(id)

            except Exception as e:
                flash("Broken URL. Aborted")
                abort(404)

            if comment['authorId'] == current_user.user['id']:
                delete = Delete()
                try:
                    delete.delete_task_comment(int(id))
                    flash("Comment deleted")
                    return redirect(url_for('tasks'))
                except Exception as e:
                    flash("Error while deleting comment")
                    return redirect(url_for('tasks'))
            else:
                flash("You are not authorized to perform this action")
                return redirect(url_for('tasks'))
        else:
            flash("Login to delete comment")
            return redirect(url_for('login'))

    return redirect(url_for('tasks'))

# Delete a heat comment if the authorId is the current user
@app.route('/delete_heat_comment', strict_slashes=False, methods=['POST', 'GET'])
def delete_heat_comment():
    """Deletes a heat comment if the authorId is the current user
    """
    if request.args.get('id'):
        try:
            id = int(request.args.get('id'))
        except ValueError:
            flash("Bad argument")
            abort(400)

        if current_user.is_authenticated:
            try:
                comment = get_article_comment(id)

            except Exception as e:
                flash("Broken URL. Aborted")
                abort(404)

            if comment['authorId'] == current_user.user['id']:
                delete = Delete()
                try:
                    delete.delete_heat_comment(int(id))
                    flash("Comment deleted")
                    return redirect(url_for('wellness'))
                except Exception as e:
                    flash("Error while deleting comment")
                    return redirect(url_for('wellness'))
            else:
                flash("You are not authorized to perform this action")
                return redirect(url_for('wellness'))
        else:
            flash("Login to delete comment")
            return redirect(url_for('login'))

    return redirect(url_for('wellness'))

# Route for fun, Include my details
@app.route('/dev', strict_slashes=False)
def dev():
    """Return the dev.html template
    """

    return render_template('dev.html', title="Dev")


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
            return redirect(url_for('index'))
        elif user['password'] != password:
            flash('Invalid password')
            return redirect(url_for('login'))

        elif user['username'] != username:
            flash('Invalid username')
            return redirect(url_for('login'))

        else:
            flash('Invalid username and password')

            return redirect(url_for('login'))
    else:
        flash("User doesn't exist")
        return redirect('/register')


# Return if the user is logged in
def is_logged_in():
    return current_user.is_authenticated

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
