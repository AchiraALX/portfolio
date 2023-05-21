#!/usr/bin/env python3
""" The DataBase Storage
"""
from models.base import Base
from models.blog import Blog, BlogComment
from models.heat import Heat, HeatComment
from models.task import Task, TaskComment
from models.repo import Repo
from models.user import User
from models.ghub import Ghub
from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import Session
from datetime import datetime


class DBStorage:
    """Data Base Storage class.
    """

    engine = None
    session = None


    # Initialize class
    def __init__(self):
        # Create connection to the database
        self.engine = create_engine(
            'mysql+pymysql://diary:diarydb@localhost/portfolio'
        )

        # Create all tables
        Base.metadata.create_all(self.engine)

        # Create a new session
        self.session = Session(bind=self.engine)

    @staticmethod
    def _class(_class: str):
        classes = {
            'blog': Blog,
            'blog_comment': BlogComment,
            'task': Task,
            'task_comment': TaskComment,
            'heat': Heat,
            'heat_comment': HeatComment,
            'repo': Repo,
            'user': User,
            'ghub': Ghub
        }

        return classes[_class]

    def n_session(self):
        """session method
        Object:
            Creates the current session
        """
        return self.session

    def query_all(
            self,
            limit: int, model: str) -> str:
        """query_all

        dict:
            dictionary object representation of objects
            of a particular model

        args:
            limit: defines how many objects can be returned at a time(10, 5)
            model: specifies the table to be queried ("users", "blog")
            filter: specifies the criteria of the query ("date")
        """

        model = self._class(model)

        return self.n_session().execute(select(model))

    def query_one(self, model: str):
        """query_one: DB method

            dict: dictionary object representation of a
            queried abject of a particular model

            args:
                model: specifies the table and row to be queried (table.row)
        """
    def commit(self):
        """commit: model method

        None:
            The method will be responsible for applying changes
            in the current session
        """
    def discard(self):
        """discard instance

        None:
            The method will discard changes staged in the current
            session
        """
    def __str__(self) -> str:
        return "Database storage"

    def __repr__(self) -> str:
        return super().__repr__()


user1 = User(
    username='user1',
    email='user1@example.com',
    password='password1',
    name='User 1',
    gender='M'
)
user2 = User(
    username='user2',
    email='user2@example.com',
    password='password2',
    name='User 2',
    gender='F',
    reg_date=datetime.utcnow(),
    last_login=datetime.utcnow()
)
blog1 = Blog(
    blog_title='Blog 1',
    blog_content='This is blog 1 content',
    author=user1
)
heat1 = Heat(
    title='Heat 1',
    content='This is heat 1 content',
    published_date=datetime.utcnow(),
    author=user2
)
comm = HeatComment(
    comment="I like this kind of .....",
    comment_date=datetime.utcnow(),
    author=user1,
    heat=heat1
)

db = DBStorage()
ses = db.n_session()

#ses.add(user1)


#print(ses.new)
#ses.flush()

#person = ses.get(User, user1.id)
#print(person == user1)

#ses.commit()


jacob = db.query_all(10, "user")
u3 = ses.execute(select(User).filter_by(name="User 3")).scalar_one()
print(u3)

ses.delete(u3)
ses.flush()
print(u3 in ses)

for row in jacob:
    obj = row[0]
    print(obj)
    #print(f"ID: {obj.id}, name: {obj.name}, email: {obj.email}, username: {obj.username}")

ses.rollback()
print(u3 in ses)

user = db._class("blog")
print(user)
