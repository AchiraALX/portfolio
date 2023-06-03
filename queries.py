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
def get_blog():
    """Fetch a blog from the database
    """
    pass

blogs = main("blogs")

print(blogs)


#
# Copyright
# Jacob Achira Obara
# 2023
#
