#!/usr/bin/env python3
"""Definition of GraphQL API using graphene
"""

import graphene
from graphene import (
    ObjectType,
    String,
    Schema,
    Field,
    List,
    Int,
    DateTime
)
from datetime import datetime
from db_storage import DBStorage
from models.user import User
from models.task import Task, TaskComment
from models.blog import Blog, BlogComment
from models.heat import Heat, HeatComment
from models.repo import Repo
from models.ghub import Ghub
import json


# Define the User type
class UserType(ObjectType):
    """UserType class. Creates type for User

    Args:
        ObjectType (Inherited): graphene ObjectType
    """
    id = Int()
    username = String()
    name = String()
    email = String()
    password = String()
    gender = String()
    reg_date = DateTime()
    last_login = DateTime()


# Define TaskType
class TaskType(ObjectType):
    """TaskType class. Creates type for Task

    Args:
        ObjectType (Inherited): graphene ObjectType
    """
    id = Int()
    title = String()
    description = String()
    status = String()
    task_due_date = DateTime()
    task_created_date = DateTime()
    task_last_modified_date = DateTime()


# Define BlogType
class BlogType(ObjectType):
    """BlogType class. Creates type for Blog

    Args:
        ObjectType (Inherited): graphene ObjectType
    """
    id = Int()
    blog_title = String()
    blog_content = String()
    blog_published_date = DateTime()


# Define HeatType
class HeatType(ObjectType):
    """HeatType class. Creates type for Heat

    Args:
        ObjectType (Inherited): graphene ObjectType
    """
    id = Int()
    title = String()
    content = String()
    published_date = DateTime()
    last_modified_date = DateTime()


# Define RepoType
class RepoType(ObjectType):
    """RepoType class. Creates type for Repo

    Args:
        ObjectType (Inherited): graphene ObjectType
    """
    id = Int()
    repository_name = String()
    repository_url = String()
    repository_description = String()


# Define GhubType
class GhubType(ObjectType):
    """GhubType class. Creates type for Ghub

    Args:
        ObjectType (Inherited): graphene ObjectType
    """
    id = Int()
    repos_num = Int()
    followers = Int()
    stars = Int()
    description = String()
    last_refreshed = DateTime()


# Define TaskCommentType
class TaskCommentType(ObjectType):
    """TaskCommentType class. Creates type for TaskComment

    Args:
        ObjectType (Inherited): graphene ObjectType
    """
    id = Int()
    task_comment = String()
    task_comment_date = DateTime()
    last_modified_date = DateTime()


# Define BlogCommentType
class BlogCommentType(ObjectType):
    """BlogCommentType class. Creates type for BlogComment

    Args:
        ObjectType (Inherited): graphene ObjectType
    """
    id = Int()
    blog_comment = String()
    blog_comment_date = DateTime()
    last_modified_date = DateTime()


# Define HeatCommentType
class HeatCommentType(ObjectType):
    """HeatCommentType class. Creates type for HeatComment

    Args:
        ObjectType (Inherited): graphene ObjectType
    """
    id = Int()
    comment = String()
    comment_date = DateTime()
    last_modified_date = DateTime()


class Query(ObjectType):
    """Query class

    Args:
        ObjectType (Inherited): graphene ObjectType

    Returns:
        resolve_user: users query
        resolve_task: tasks query
        resolve_blog: blogs query
        resolve_heat: heats query
        resolve_repo: repos query
        resolve_ghub: ghub query
        resolve_task_comment: task_comments query
        resolve_blog_comment: blog_comments query
        resolve_heat_comment: heat_comments query
    """
    users = List(UserType)
    tasks = List(TaskType)
    blogs = List(BlogType)
    heats = List(HeatType)
    repos = List(RepoType)
    ghub = List(GhubType)
    task_comments = List(TaskCommentType)
    blog_comments = List(BlogCommentType)
    heat_comments = List(HeatCommentType)

    def resolve_users(self, info):
        """resolve_users method. Resolves users query

        Args:
            info (obj): GraphQL info object

        Returns:
            list object: users list
        """

        # return list of users
        db = DBStorage()
        session = db.n_session()

        # Query users from the database
        users = session.query(User).all()

        users_list = [user.__dict__ for user in users]

        # Close the session
        session.close()

        return users_list

    def resolve_tasks(self, info):
        """resolve_tasks method. Resolves tasks query

        Args:
            info (object): GraphQL info object

        Returns:
            list object: tasks list
        """
        # return list of tasks
        db = DBStorage()
        session = db.n_session()

        # Query tasks from the database
        tasks = session.query(Task).all()

        tasks_list = [task.__dict__ for task in tasks]

        # Close the session
        session.close()

        return tasks_list

    def resolve_blogs(self, info):
        """resolve_blogs method. Resolves blogs query

        Args:
            info (object): GraphQL info object

        Returns:
            list object: blogs list
        """
        # return list of blogs
        db = DBStorage()
        session = db.n_session()

        # Query blogs from the database
        blogs = session.query(Blog).all()

        blogs_list = [blog.__dict__ for blog in blogs]

        # Close the session
        session.close()

        return blogs_list

    def resolve_heats(self, info):
        """resolve_heats method. Resolves heats query

        Args:
            info (object): GraphQL info object

        Returns:
            list object: heats list
        """
        # return list of heats
        db = DBStorage()
        session = db.n_session()

        # Query heats from the database
        heats = session.query(Heat).all()

        heats_list = [heat.__dict__ for heat in heats]

        # Close the session
        session.close()

        return heats_list

    def resolve_repos(self, info):
        """resolve_repos method. Resolves repos query

        Args:
            info (object): GraphQL info object

        Returns:
            list object: repos list
        """
        # return list of repos
        db = DBStorage()
        session = db.n_session()

        # Query repos from the database
        repos = session.query(Repo).all()

        repos_list = [repo.__dict__ for repo in repos]

        # Close the session
        session.close()

        return repos_list

    def resolve_ghub(self, info):
        """resolve_ghub method. Resolves ghub query

        Args:
            info (object): GraphQL info object

        Returns:
            list object: ghub list
        """
        # return list of ghub
        db = DBStorage()
        session = db.n_session()

        # Query ghub from the database
        ghub = session.query(Ghub).all()

        ghub_list = [ghub.__dict__ for ghub in ghub]

        # Close the session
        session.close()

        return ghub_list

    def resolve_task_comments(self, info):
        """resolve_task_comments method. Resolves task_comments query

        Args:
            info (object): GraphQL info object

        Returns:
            list object: task_comments list
        """
        # return list of task_comments
        db = DBStorage()
        session = db.n_session()

        # Query task_comments from the database
        task_comments = session.query(TaskComment).all()

        task_comments_list = [
            task_comment.__dict__ for task_comment in task_comments
        ]

        # Close the session
        session.close()

        return task_comments_list

    def resolve_blog_comments(self, info):
        """resolve_blog_comments method. Resolves blog_comments query

        Args:
            info (object): GraphQL info object

        Returns:
            list object: blog_comments list
        """
        # return list of blog_comments
        db = DBStorage()
        session = db.n_session()

        # Query blog_comments from the database
        blog_comments = session.query(BlogComment).all()

        blog_comments_list = [
            blog_comment.__dict__ for blog_comment in blog_comments
        ]

        # Close the session
        session.close()

        return blog_comments_list

    def resolve_heat_comments(self, info):
        """resolve_heat_comments method. Resolves heat_comments query

        Args:
            info (object): GraphQL info object

        Returns:
            list object: heat_comments list
        """
        # return list of heat_comments
        db = DBStorage()
        session = db.n_session()

        # Query heat_comments from the database
        heat_comments = session.query(HeatComment).all()

        heat_comments_list = [
            heat_comment.__dict__ for heat_comment in heat_comments
        ]

        # Close the session
        session.close()

        return heat_comments_list


schema = Schema(query=Query)

if __name__ == "__main__":
    query = '''
    {
        users {
            id
            username
            name
            email
            gender
            regDate
            lastLogin
        }
    }
    '''
    task = '''
    {
        tasks {
            id
            title
            description
            status
            taskDueDate
        }
    }
    '''
    blog = '''
    {
        blogs {
            id
            blogTitle
            blogContent
            blogPublishedDate
        }
    }
    '''
    heat = '''
    {
        heats {
            id
            title
            content
            publishedDate
        }
    }
    '''

    result = schema.execute(heat)
    if result.errors:
        print(result.errors)
    else:
        result_dict = dict(result.data.items())
        print(json.dumps(result_dict, indent=2))
