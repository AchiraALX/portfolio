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

class Add:
    """Class for add methods
    """

    user = None
    task = None
    task_comment = None
    repo = None
    heat = None
    heat_comment = None
    ghub = None
    blog = None
    blog_comment = None

    all_classes = (
        user,
        task,
        task_comment,
        repo,
        heat,
        heat_comment,
        ghub,
        blog,
        blog_comment
    )
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
        gender: str =None,
        password: str = None
    ) -> User:
        details = {
            'name': name,
            'username': username,
            'email': email,
            'gender': gender,
            'password': password
        }

        for key, value in details.items():
            if value == None:
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
            return f"\nSome values failed {self.failed} and the user was not added."

        else:
            user = User(**details)
            if self.add_to_database(user) == None:
                print(f"Added user as successfully!")

        return User(**details) if User(**details) else None

    def add_blog(
        self,
        blog_title = None,
        blog_content = None,
        author = None
    ) -> Blog:
        details = {
            'blog_title': blog_title,
            'blog_content': blog_content,
            'author': author
        }

        for key, value in details.items():
            if value == None:
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
        task_title = None,
        task_description = None,
        task_status = None,
        task_assignee = None
        ) -> Task:

        details = {
            'task_title': task_title,
            'task_description': task_description,
            'task_status': task_status,
            'task_assignee': task_assignee,
            'task_due_date': self.time_now()
        }

        for key, value in details.items():
            if value == None:
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
        title = None,
        content = None,
        author=None
    ) -> Heat:
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
        repos = None,
        followers = None,
        stars = None,
        description = None,
        owner_info = None
    ) -> Ghub:
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
        repository_name = None,
        repository_url = None,
        repository_description = None,
        author_id = None
    ) -> Repo:
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
        task_comment = None,
        task = None,
        author = None
    ) -> TaskComment:
        details = {
            'task_comment': task_comment,
            'task': task,
            'author': author
        }

        return self.check_for_none_and_add_to_db(
            details, TaskComment, 'task comment', 'author'
        )

    def ensure_obj_present(
        self,
        model,
        filter: dict,

    ):
        parent = self.ses.query(model).filter_by(**filter).first()

        if parent:
            return parent

    def check_for_int(self, value):
        while True:
            try:
                value = int(value)
                break
            except ValueError:
                print("Value must be an integer!")
                value = self.add_field('num')

        return value

    def check_for_none_and_add_to_db(
        self,
        details: dict,
        model,
        df,
        special = [],
        int_fields: list = [],
    ):
        for key, value in details.items():
            if value == None:
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

    def ensure_user_present(self, name, field = 'username'):
        while not self.get_user(name):
            print(f"No valid user with username {name}!")
            name = self.add_field(field)

        return name

    def time_now(self):
        return datetime.utcnow().strftime("%Y:%m:%d %H:%M:%S")

    def get_user(self, username):
        user = self.ses.query(User).filter_by(username=username).first()
        return user

    def unpack_and_add_to_db(self, details, model, df):
        if len(self.failed) == 0:
            pack = model(**details)
            if self.add_to_database(pack) == None:
                print(f"Added {df} as successfully!")
        else:
            print(f"Some values failed {self.failed}. Check and try again!")
            return None

        return model(**details) if model(**details) else None


    def add_to_database(self, model):
        db = self.db
        db.commit(model)

    def check_for_validity(self, string) -> bool:
        s = str(string)
        s = string.strip().split(' ')
        if s == ['']:
            return False

        return True

    def check_email(self, email):
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

    def check_password(self, password):
        if len(password) < 8:
            return False
        return True

    def add_field(self, field):
        return input(f"Enter {field!r}: ")

    def __repr__(self) -> str:
        for c in self.all_classes:
            if c != None:
                return f"{dict(c)}"

if __name__ == "__main__":
    add = Add()
    print(add.add_repo())
