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
from models.token import Token
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
        model = self._class(model)

        return self.n_session().execute(select(model))

    def commit(self, obj):
        """commit: model method

        None:
            The method will be responsible for applying changes
            in the current session
        """
        ses = self.n_session()
        try:
            ses.add(obj)
            ses.flush()
            ses.commit()

            return obj

        except Exception as e:
            ses.rollback()
            raise e

    def discard(self):
        """discard instance

        None:
            The method will discard changes staged in the current
            session
        """

        ses = self.n_session()
        try:
            ses.rollback()
        except Exception as e:
            raise e

    def close_session(self):
        """close_session instance

        description:
            The method will close the current session
        """

        return self.n_session().close()

    def __str__(self) -> str:
        # Check for engine connection
        messages = [
            "You can add new objects to the database",
            "You can't add new objects to the database"
        ]
        ses_status = "Connected" if self.engine else "Not connected"
        message = messages[0] if self.engine else messages[1]
        return f"<DBStorage: {ses_status}> {message!r}"

    def __repr__(self) -> str:
        ses = self.n_session()

        # Check for uncommitted changes
        if ses.new:
            return f"<DBStorage: {ses}>"

        else:
            # No uncommitted changes? Return last committed object
            model_classes = [
                Blog, BlogComment, Task, TaskComment,
                Heat, HeatComment, Repo, User, Ghub
            ]

            for model in model_classes:
                last_committed_obj = ses.query(model)\
                    .order_by(model.id.desc()).first()
                if last_committed_obj:
                    break

            return "<DBStorage: {}>".format(last_committed_obj)


if __name__ == "__main__":
    db = DBStorage()
    user = db.n_session().query(User).filter_by(id=26).first()
    token = Token(
        token="alkjfhalsjkdfasd",
        user_info=user
    )

    db.commit(token)
    print(db.n_session().query(Token).all())


#
# Copyright
# Jacob Achira Obara
# 2023
#
