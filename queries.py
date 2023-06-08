#!/usr/bin/env python3
"""Queries"""

from resolvers import *

users = main("users")['users']

def query_user(username: str) -> dict:
    """Return user details

    Args:
        username (str): username

    Returns:
        dict: _description_
    """

    for user in users:
        if user['username'] == username:
            return user

    return None

# Get blogs
def get_blog(id: int):
    """Fetch a blog from the database
    """
    blogs = main("blogs")['blogs']

    for blog in blogs:
        if blog['id'] == id:
            return blog

    return None

# Get health article
def get_article(id: int):
    """Fetch a health article from the database
    """
    articles = main("heats")['heats']

    for article in articles:
        if article['id'] == id:
            return article

    return None

# Query single task
def get_task(id):
    """Fetch a single task
    """

    tasks = main('tasks')['tasks']

    for task in tasks:
        if task['id'] == id:
            return task

    return None

# Get ghubs matching id
def get_ghub(id):
    """Fetch a single ghub
    """

    ghubs = main('ghub')['ghub']
    # List for the ghubs
    hubs = []

    for ghub in ghubs:
        if ghub['ownerId'] == id:
            hubs.append(ghub)

    return hubs


# Get all repos matching id
def get_repos(id):
    """Fetch a single repo
    """

    repos = main('repos')['repos']
    # List for the repos
    repositories = []

    for repo in repos:
        if repo['ownerId'] == id:
            repositories.append(repo)

    return repositories

# Get comment per specified blog id
def get_blog_comments(id):
    """Get comment that belong to blog with id equal to id

    Args:
        id (int): The id of the blog
    """

    all_comments = main('blog_comments')['blogComments']
    comments_available = []
    for comment in all_comments:
        if comment['blogId'] == id:
            comments_available.append(comment)

    return comments_available

# Get comment per specified article id
def get_article_comments(id):
    """Get comment that belong to article with id equal to id

    Args:
        id (int): The id of the article
    """

    all_comments = main('heat_comments')['heatComments']
    comments_available = []
    for comment in all_comments:
        if comment['heatId'] == id:
            comments_available.append(comment)

    return comments_available

# Get repositories per specified ghub id
def get_user_repos(id):
    """Get repositories that belong to ghub with id equal to id

    Args:
        id (int): The id of the ghub
    """

    all_repos = main('repos')['repos']
    repos_available = []
    for repo in all_repos:
        if repo['ownerId'] == id:
            repos_available.append(repo)

    return repos_available

# Get a single blog comment
def get_blog_comment(id):
    """Get a single blog comment

    Args:
        id (int): The id of the blog comment
    """

    all_comments = main('blog_comments')['blogComments']
    for comment in all_comments:
        if comment['id'] == id:
            return comment

    return None

# Get a single article comment
def get_article_comment(id):
    """Get a single article comment

    Args:
        id (int): The id of the article comment
    """

    all_comments = main('heat_comments')['heatComments']
    for comment in all_comments:
        if comment['id'] == id:
            return comment

    return None

# Get a single task comment
def get_task_comment(id):
    """Get a single task comment

    Args:
        id (int): The id of the task comment
    """

    all_comments = main('task_comments')['taskComments']
    for comment in all_comments:
        if comment['id'] == id:
            return comment

    return None

print(get_blog(18))


#
# Copyright
# Jacob Achira Obara
# 2023
#
