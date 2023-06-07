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




#
# Copyright
# Jacob Achira Obara
# 2023
#
