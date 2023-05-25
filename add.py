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

        details = self.add_comment(
            details, 'task'
        )

        return self.unpack_and_add_to_db(
            details, TaskComment, 'task comment'
        )

    def add_blog_comment(
        self,
        comment = None,
        blog = None,
        author = None
    ) -> BlogComment:
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
        comment = None,
        heat = None,
        author = None
    ) -> HeatComment:
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

    def add_comment(
        self,
        details: dict,
        spec: str
    ):

        for key, value in details.items():
            if value == None:
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
                                blog = value
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

    def get_task(self, id):
        id = id
        obj =lambda id: self.ses.query(Task).filter_by(id=id).first()

        while not obj(id):
            print("Enter a valid task id.")
            id = self.add_field('task_id')

        return obj(id)


    def get_blog(self, id):
        id = id
        obj =lambda id: self.ses.query(Blog).filter_by(id=id).first()

        while not obj(id):
            print("Enter a valid blog id.")
            id = self.add_field('blog_id')

        return obj(id)

    def get_heat(self, id):
        id = id
        obj = lambda id: self.ses.query(Heat).filter_by(id=id).first()

        while not obj(id):
            print("Enter a valid Health article id")
            id = self.add_field('health_article_id')

        return obj(id)

    def ensure_obj_present(
        self,
        task = None,
        blog = None,
        heat = None
    ) -> int:
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

    def check_for_int(self, value, key = None) -> int:
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
    print(add.add_heat_comment())
