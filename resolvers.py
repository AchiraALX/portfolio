#!/usr/bin/env python3
"""Definition of GraphQL API using graphene
"""

import graphene
from graphene import (
    ObjectType,
    String,
    Schema,
    List,
    Int,
    DateTime
)
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
    blogs = List(lambda: BlogType)
    tasks = List(lambda: TaskType)
    heats = List(lambda: HeatType)
    blog_comments = List(lambda: BlogCommentType)
    heat_comments = List(lambda: HeatCommentType)
    task_comments = List(lambda: TaskCommentType)
    repos = List(lambda: RepoType)
    ghub = List(lambda: GhubType)


# Define TaskType
class TaskType(ObjectType):
    """TaskType class. Creates type for Task

    Args:
        ObjectType (Inherited): graphene ObjectType
    """
    id = Int()
    task_title = String()
    task_description = String()
    task_status = String()
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
    repos = Int()
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
    comment = String()
    comment_date = DateTime()
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

        # Blogs filter by user id
        blogs = session.query(Blog).all()

        # Tasks filter by user id
        tasks = session.query(Task).all()

        # Heats filter by user id
        heats = session.query(Heat).all()

        # Repos filter by user id
        repos = session.query(Repo).all()

        # Ghub filter by user id
        ghubs = session.query(Ghub).all()

        # TaskComments filter by user id
        task_comments = session.query(TaskComment).all()

        # BlogComments filter by user id
        blog_comments = session.query(BlogComment).all()

        # HeatComments filter by user id
        heat_comments = session.query(HeatComment).all()

        users_list = [user.__dict__ for user in users]

        # Add blogs,  to users_list
        for user in users_list:
            user['blogs'] = [
                blog.__dict__ for blog in blogs if blog.author_id == user[
                    'id'
                ]
            ]
            user['tasks'] = [
                task.__dict__ for task in tasks if task.assignee_id == user[
                    'id'
                ]
            ]
            user['heats'] = [
                heat.__dict__ for heat in heats if heat.author_id == user[
                    'id'
                ]
            ]
            user['repos'] = [
                repo.__dict__ for repo in repos if repo.owner_id == user[
                    'id'
                ]
            ]
            user['ghub'] = [
                ghub.__dict__ for ghub in ghubs if ghub.owner_id == user[
                    'id'
                ]
            ]
            user[
                'task_comments'
            ] = [
                task_comment.__dict__ for task_comment in
                task_comments if task_comment.author_id == user[
                    'id'
                ]
            ]
            user[
                'blog_comments'
            ] = [
                blog_comment.__dict__ for blog_comment in
                blog_comments if blog_comment.author_id == user[
                    'id'
                ]
            ]
            user[
                'heat_comments'
            ] = [
                heat_comment.__dict__ for heat_comment in
                heat_comments if heat_comment.author_id == user[
                    'id'
                ]
            ]

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


# GraphQL query execution method
def execute_query(query):
    """execute_query method. Executes GraphQL query

    Args:
        query (str): GraphQL query

    Returns:
        dict object: query result
    """
    result = schema.execute(query)
    if result.errors:
        print(result.errors)
    else:
        result_dict = dict(result.data.items())
        return result_dict


def main(query: str = None) -> dict:
    """Main method. Executes GraphQL query

    Keyword arguments:
    query -- GraphQL query (default None)

    Return: dict object
    """

    users = '''
    {
        users {
            id
            username
            name
            email
            gender
            regDate
            lastLogin
            password
            blogs {
                id
                blogTitle
            }
            tasks {
                id
                taskTitle
            }
            heats {
                id
                title
            }
            heatComments {
                id
                comment
            }
            blogComments {
                id
                comment
            }
            taskComments {
                id
                taskComment
            }
            repos {
                id
                repositoryName
                repositoryUrl
            }
            ghub {
                id
                description
            }
        }
    }
    '''
    tasks = '''
    {
        tasks {
            id
            taskTitle
            taskDescription
            taskStatus
            taskDueDate
        }
    }
    '''
    blogs = '''
    {
        blogs {
            id
            blogTitle
            blogContent
            blogPublishedDate
        }
    }
    '''
    heats = '''
    {
        heats {
            id
            title
            content
            publishedDate
            lastModifiedDate
        }
    }
    '''
    repos = '''
    {
        repos {
            id
            repositoryName
            repositoryDescription
            repositoryUrl
        }
    }
    '''
    ghub = '''
    {
        ghub {
            id
            repos
            followers
            stars
            description
            lastRefreshed
        }
    }
    '''
    heat_comments = '''
    {
        heatComments {
            id
            comment
        }
    }
    '''
    blog_comments = '''
    {
        blogComments {
            id
            comment
        }
    }
    '''
    task_comments = '''
    {
        taskComments {
            id
            taskComment
        }
    }
    '''
    usernames = '''
    {
        users {
            username
        }
    }
    '''

    query_list = {
        'users': users,
        'tasks': tasks,
        'blogs': blogs,
        'heats': heats,
        'repos': repos,
        'ghub': ghub,
        'heat_comments': heat_comments,
        'blog_comments': blog_comments,
        'task_comments': task_comments,
        'usernames': usernames
    }

    for key, value in query_list.items():
        if query == key:
            data = execute_query(value)
            break

    return json.loads(json.dumps(data))


if __name__ == "__main__":
    print(main('users'))


#
# Copyright
# Jacob Achira Obara
# 2023
#
