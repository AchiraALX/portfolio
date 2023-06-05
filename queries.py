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



#
# Copyright
# Jacob Achira Obara
# 2023
#
