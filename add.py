#!/usr/bin/env python3
"""The script will be used to add a new data to the database.
"""

from db_storage import DBStorage
from datetime import datetime
import getpass
from models.blog import Blog, BlogComment
from models.ghub import Ghub
from models.heat import Heat, HeatComment
from models.repo import Repo
from models.task import Task, TaskComment
from models.user import User
from models.token import Token


class Add:
    """Class for add methods
    """

    all_classes = {
        'user': User,
        'task': Task,
        'task_comment': TaskComment,
        'repo': Repo,
        'heat': Heat,
        'heat_comment': HeatComment,
        'ghub': Ghub,
        'blog': Blog,
        'blog_comment': BlogComment
    }
    failed = []

    def __init__(self):
        """Initialize the database
        """
        self.db = DBStorage()
        self.ses = self.db.n_session()

    def add_user(
        self,
        name: str = None,
        username: str = None,
        email: str = None,
        gender: str = None,
        password: str = None
    ) -> User:
        """Add a new user to the database

        Keyword arguments:
        name -- name of the user
        username -- username of the user
        email -- email of the user
        gender -- sex of the user
        password -- password of the user

        Return: User object
        """

        details = {
            'name': name,
            'username': username,
            'email': email,
            'gender': gender,
            'password': password
        }

        for key, value in details.items():
            if value is None:
                value = input(f"Enter {key!r}: ")\
                    if key != 'password' else \
                    getpass.getpass("Enter a password: ")

            if self.check_for_validity(value):
                if key == 'email':
                    if not self.check_email(value):
                        while not self.check_email(value):
                            print("Email must be valid, example@domain.com")
                            value = input("Enter email: ")
                if key == 'password':
                    while not self.check_password(value):
                        print("Use more than 8 characters")
                        value = getpass.getpass("Enter a password: ")

                if key == 'gender':
                    value = value.upper()

                if key == 'name':
                    value = value.capitalize()

                details[key] = value

            else:
                self.failed.append(key)

        if len(self.failed) != 0:
            return (
                f"\nSome values failed {self.failed}."
            )

        else:
            user = User(**details)
            if self.add_to_database(user) is None:
                print(f"Added user as successfully!")

        return User(**details) if User(**details) else None

    def add_blog(
        self,
        blog_title: str = None,
        blog_content: str = None,
        author: str = None
    ) -> Blog:
        """Add blog to the database.

        Keyword arguments:
        blog_title -- the title of the blog
        blog_content -- the content of the blog
        author -- the author of the blog

        Return: a Blog object
        """

        details = {
            'blog_title': blog_title,
            'blog_content': blog_content,
            'author': author
        }

        for key, value in details.items():
            if value is None:
                value = self.add_field(key)

            if self.check_for_validity(value):
                if key == 'author':
                    while not self.get_user(value):
                        print("Enter a valid username.")
                        value = self.add_field("author")

                    value = self.get_user(value)

                details[key] = value

            else:
                self.failed.append(key)

        return self.unpack_and_add_to_db(details, Blog, "blogs")

    def add_task(
        self,
        task_title: str = None,
        task_description: str = None,
        task_status: str = None,
        task_assignee=None
    ) -> Task:
        """Add task to the database.

        Keyword arguments:
        task_title -- the title of the task
        task_description -- the description of the task
        task_status -- the status of the task
        task_assignee -- the assignee of the task

        Return: a Task object
        """

        details = {
            'task_title': task_title,
            'task_description': task_description,
            'task_status': task_status,
            'task_assignee': task_assignee,
            'task_due_date': self.time_now()
        }

        for key, value in details.items():
            if value is None:
                value = self.add_field(key)

            if self.check_for_validity(value):
                if key == 'task_assignee':
                    while not self.get_user(value):
                        print("Enter a valid username.")
                        value = self.add_field(key)

                    value = self.get_user(value)

                details[key] = value
            elif key == 'task_status':
                details['task_status'] = 'pending'

            elif key == 'task_due_date':
                continue

            else:
                self.failed.append(key)

        return self.unpack_and_add_to_db(details, Task, "task")

    def add_heat(
        self,
        title: str = None,
        content: str = None,
        author=None
    ) -> Heat:
        """Add heat to the database.

        Keyword arguments:
        title -- the title of the heat
        content -- the content of the heat
        author -- the author of the heat

        Return: a Heat object
        """
        details = {
            'title': title,
            'content': content,
            'author': author
        }

        return self.check_for_none_and_add_to_db(
            details, Heat, 'health article', 'author'
        )

    def add_ghub(
        self,
        repos: int = None,
        followers: int = None,
        stars: int = None,
        description: str = None,
        owner_info=None
    ) -> Ghub:
        """Add GitHub info to the database.

        Keyword arguments:
        repos -- the number of repositories
        followers -- the number of followers
        stars -- the number of stars
        description -- the description of the user
        owner_info -- the id of the user

        Return: a Ghub object
        """

        details = {
            'repos': repos,
            'followers': followers,
            'stars': stars,
            'description': description,
            'owner_info': owner_info
        }

        int_fields = ['repos', 'followers', 'stars']

        return self.check_for_none_and_add_to_db(
            details, Ghub, 'GitHub info', 'owner_info', int_fields
        )

    def add_repo(
        self,
        repository_name: str = None,
        repository_url: str = None,
        repository_description: str = None,
        author_id=None
    ) -> Repo:
        """Add a repository to the database.

        Keyword arguments:
        repository_name -- the name of the repository
        repository_url -- the url of the repository
        repository_description -- the description of the repository
        author_id -- the id of the author of the repository

        Return: a Repo object
        """

        details = {
            'repository_name': repository_name,
            'repository_url': repository_url,
            'repository_description': repository_description,
            'author_id': author_id
        }

        return self.check_for_none_and_add_to_db(
            details, Repo, 'repository', ['author_id']
        )

    def add_task_comment(
        self,
        task_comment: str = None,
        task=None,
        author=None
    ) -> TaskComment:
        """Add a comment to a task.

        Keyword arguments:
        task_comment -- the comment to add
        task -- the task to add the comment to
        author -- the author of the comment

        Return: a TaskComment object
        """

        details = {
            'task_comment': task_comment,
            'task': task,
            'author': author
        }

        details = self.add_comment(
            details, 'task'
        )

        return self.unpack_and_add_to_db(
            details, TaskComment, 'task comment'
        )

    def add_blog_comment(
        self,
        comment: str = None,
        blog=None,
        author=None
    ) -> BlogComment:
        """Add a comment to a blog.

        Keyword arguments:
        comment -- the comment to add
        blog -- the blog to add the comment to
        author -- the author of the comment

        Return: a BlogComment object
        """

        details = {
            'comment': comment,
            'blog': blog,
            'author': author
        }

        details = self.add_comment(
            details, 'blog'
        )

        return self.unpack_and_add_to_db(
            details, BlogComment, 'blog comment'
        )

    def add_heat_comment(
        self,
        comment: str = None,
        heat=None,
        author=None
    ) -> HeatComment:
        """Add a comment to a health article.

        Keyword arguments:
        comment -- the comment to add
        heat -- the health article to add the comment to
        author -- the author of the comment

        Return: a HeatComment object
        """

        details = {
            'comment': comment,
            'heat': heat,
            'author': author
        }

        details = self.add_comment(
            details, 'heat'
        )

        return self.unpack_and_add_to_db(
            details, HeatComment, 'heat comment'
        )

    # Add token to database
    def add_token(
        self,
        token: str = None,
        user_info=None
    ) -> Token:
        """Insert a token into the database.

        Keyword arguments:
            token -- the token to insert
            user_info -- the id of the user
        """

        details = {
            'token': token,
            'user_info': user_info
        }

        token = Token(**details)

        try:
            self.db.commit(token)

        except Exception as e:
            print(e)

    def add_comment(
        self,
        details: dict,
        spec: str
    ) -> dict:
        """Add a comment to a task, blog or heat.

        Keyword arguments:
        details -- a dictionary containing the comment and spec
        spec -- the model to add the comment to (task, blog or heat)
        Return: a dictionary containing the comment, spec and author
        """

        for key, value in details.items():
            if value is None:
                value = self.add_field(key)

            if self.check_for_validity(value):
                if key == spec:
                    try:
                        if spec == 'task':
                            value = self.ensure_obj_present(
                                task=value
                            )
                        elif spec == 'blog':
                            value = self.ensure_obj_present(
                                blog=value
                            )
                        elif spec == 'heat':
                            value = self.ensure_obj_present(
                                heat=value
                            )

                        else:
                            return None

                    except RuntimeError:
                        print(f"Task with id {value!r} was not found.")
                        print("Check a retry")
                        value = None
                        self.failed.append('key')
                        return None

                if key == 'author':
                    value = self.ensure_user_present(value)
                    value = self.get_user(value)

                details[key] = value

            else:
                self.failed.append(key)

        return details

    def get_task(self, id: int) -> Task:
        """Get task method gets the task object
        from the database

        Keyword arguments:
        id -- task id
        Return: returns the task object
        """

        id = id
        obj = lambda id: self.ses.query(Task).filter_by(id=id).first()

        while not obj(id):
            print("Enter a valid task id.")
            id = self.add_field('task_id')

        return obj(id)

    def get_blog(self, id: int) -> Blog:
        """Get blog method gets the blog object
        from the database

        Keyword arguments:
        id -- blog id
        Return: returns the blog object
        """

        id = id
        obj = lambda id: self.ses.query(Blog).filter_by(id=id).first()

        while not obj(id):
            print("Enter a valid blog id.")
            id = self.add_field('blog_id')

        return obj(id)

    def get_heat(self, id: int) -> Heat:
        """Get heat method gets the health article object
        from the database

        Keyword arguments:
        id -- health article id
        Return: returns the health article object
        """

        id = id
        obj = lambda id: self.ses.query(Heat).filter_by(id=id).first()

        while not obj(id):
            print("Enter a valid Health article id")
            id = self.add_field('health_article_id')

        return obj(id)

    def ensure_obj_present(
        self,
        task=None,
        blog=None,
        heat=None
    ) -> int:
        """Ensure obj present method ensures that the
        object is present in the database

        Keyword arguments:
        task -- task id
        blog -- blog id
        heat -- health article id
        Return: returns the object
        """

        details = {
            'task': task,
            'blog': blog,
            'heat': heat
        }

        for key, value in details.items():
            if value is not None:
                if key == 'task':
                    value = self.get_task(value)
                elif key == 'blog':
                    value = self.get_blog(value)
                elif key == 'heat':
                    value = self.get_heat(value)
                else:
                    continue

                return value

        return None

    def check_for_int(self, value, key=None) -> int:
        """Check for int method checks for
        int values in the details dictionary and the input
        fields

        Keyword arguments:
        value -- value to be checked
        key -- description of the field
        Return: returns the value
        """

        while True:
            try:
                value = int(value)
                break
            except ValueError:
                print(f" {key!r} must be an integer!")
                value = self.add_field(key)

        return value

    def check_for_none_and_add_to_db(
        self,
        details: dict,
        model,
        df,
        special: list = [],
        int_fields: list = [],
    ):
        """Check for none and add to db method checks for
        none values in the details dictionary and adds
        them to the database

        Keyword arguments:
        details -- details dictionary
        model -- model to be added to the database
        df -- description of the model
        special -- fields that will be ensured to be present
        int_fields -- fields that will be checked for int

        Return: returns the model object
        """

        for key, value in details.items():
            if value is None:
                value = self.add_field(key)

            if self.check_for_validity(value):
                if key in special:
                    value = self.ensure_user_present(value, key)
                    value = self.get_user(value)

                if key in int_fields:
                    value = self.check_for_int(value)

                details[key] = value

            else:
                self.failed.append(key)

        return self.unpack_and_add_to_db(details, model, df)

    def ensure_user_present(
        self, name: str, field: str = 'username'
    ) -> str:
        """Ensure user present method ensures that the
        user is present in the database

        Keyword arguments:
        name -- name of the user to be ensured
        field -- field to be added to the database
        Return: returns the name of the user
        """

        while not self.get_user(name):
            print(f"No valid user with username {name}!")
            name = self.add_field(field)

        return name

    def time_now(self):
        """Time now method gets the current time

        Return: string representation of the current time
        """

        return datetime.utcnow().strftime("%Y:%m:%d %H:%M:%S")

    def get_user(self, username: str):
        """Get user method gets the user from the database

        Keyword arguments:
        username -- username of the user to be gotten
        Return: returns the user if found else None
        """

        user = self.ses.query(User).filter_by(username=username).first()
        return user if user else None

    def unpack_and_add_to_db(self, details: dict, model, df: str):
        """Unpack and add to database method unpacks the details
        and adds the model to the database

        Keyword arguments:
        details -- dictionary of items to be unpacked
        model -- model to be used in adding the items
        df -- description of the model
        Return: returns the model if successful else None
        """

        if len(self.failed) == 0:
            pack = model(**details)
            if self.add_to_database(pack) is None:
                print(f"Added {df} as successfully!")
        else:
            print(f"Some values failed {self.failed}. Check and try again!")
            return None

        return model(**details) if model(**details) else None

    def add_to_database(self, model) -> None:
        """Add to database method adds the model to the database

        Keyword arguments:
        model -- model to be added to the database
        Return: None
        """

        db = self.db
        db.commit(model)

    def check_for_validity(self, string: str) -> bool:
        """Check for validity method checks if the string
        is valid i.e not empty

        Keyword arguments:
        string -- string to be checked
        Return: True if string is valid else False
        """

        s = str(string)
        s = string.strip().split(' ')
        if s == ['']:
            return False

        return True

    def check_email(self, email: str) -> bool:
        """Check email method checks if the email
        is valid i.e contains @ and .com

        Keyword arguments:
        email -- email to be checked
        Return: True if email is valid else False
        """

        try:
            email = email.split('@')
            try:
                domain = email[1].split('.')
            except IndexError:
                return False
            if len(domain) < 2:
                return False
            return True
        except AttributeError as e:
            return False

    def check_password(self, password: str) -> bool:
        """Check password method checks if the password
        is valid. basically > 8 characters

        Keyword arguments:
        password -- A string to be checked
        Return: True if password is valid else False
        """

        if len(password) < 8:
            return False
        return True

    def add_field(self, field) -> str:
        """Add field method reads arguments from the
        command line and returns the input of the user

        Keyword arguments:
        field -- name of the field to be added
        Return: returns the input of the user
        """

        return input(f"Enter {field!r}: ")

    def __repr__(self) -> str:
        """This is the representation of the class method

        Returns:
            str: Representation of the class
        """
        for c in self.all_classes:
            if c is not None:
                return f"{dict(c)}"


def main(model: str = None, items: dict = None):
    """This is the main function

    Keyword arguments:
    model -- This is the model to be used
    items -- This a dictionary of items to be added
    Return: None if model of items is None or model
            does not match any cases
    """
    if model is None or items is None:
        return None

    add = Add()
    if model == 'user':
        return add.add_user(**items)

    elif model == 'task':
        return add.add_task(**items)

    elif model == 'blog':
        return add.add_blog(**items)

    elif model == 'repo':
        return add.add_repo(**items)

    elif model == 'ghub':
        return add.add_ghub(**items)

    elif model == 'heat':
        return add.add_heat(**items)

    elif model == 'heatComment':
        return add.add_heat_comment(**items)

    elif model == 'blogComment':
        return add.add_blog_comment(**items)

    elif model == 'taskComment':
        return add.add_task_comment(**items)

    else:
        pass

    return None


if __name__ == '__main__':
    add = Add()
    user = add.get_user('achira')
    token = {
        'token': 'can be very new',
        'user_info': user
    }
    print(add.add_token(**token))

#
# Copyright
# Jacob Achira Obara
# 2023
#
