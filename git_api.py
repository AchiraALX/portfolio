#!/usr/bin/env python3
"""This is the GitHub API script
"""
from github import Github
import requests
from urllib.parse import urlencode, parse_qs

token = "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"
client_id = "876f14bc9874ac5be6f2"
redirect_uri = "https://www.blissprism.tech"
g = Github(token)

scope = "user:email,repo"


def get_auth_url():
    """Get authorization url
    """
    return 'https://github.com/login/oauth/authorize?' + urlencode({
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'scope': scope
    })


def get_repo_details(name):
    """Get repo details

    Args:
        name (str): Repository name

    Returns:
        dict: Repository details
    """

    try:
        repo = g.get_repo(f"AchiraALX/{name}")
        return {
            "name": repo.name,
            "description": repo.description,
            "stars": repo.stargazers_count,
            "followers": repo.get_contributors().totalCount,
            "readme": repo.get_readme().decoded_content.decode(),
            "languages": repo.get_languages(),
            "files": repo.get_contents("")
        }

    except Exception as e:
        return {
            "error": "Repository not found"
        }
