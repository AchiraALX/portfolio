#!/usr/bin/env python3
"""This is the GitHub API script
"""
from github import Github
import requests
from urllib.parse import urlencode
import json

# GitHub OAuth app credentials
file_dir = "/home/achira/Desktop/achira/token.json"
with open(file_dir) as f:
    admin_data = json.load(f)

client_id = admin_data["client_id"]
client_secret = admin_data["client_secret"]
token = admin_data["token"]
redirect_uri = "http://127.0.0.1:8000"
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

# Using the code returned by the OAuth app
def get_user_details(code):
    """Get user details

    Args:
        code (str): Code returned by the OAuth app

    Returns:
        dict: User details
    """
    global client_id
    global client_secret
    global redirect_uri

    base_url = "https://api.github.com"

    # Exchange the authorization code for access token
    token_url = "https://github.com/login/oauth/access_token"
    client_id = client_id
    client_secret = client_secret

    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": redirect_uri,
    }

    response = requests.post(
        token_url,
        data=payload,
        headers={"Accept": "application/json"}
    )

    if response.status_code == 200:
        response_data = response.json()
        if 'access_token' in response_data:
            access_token = response_data['access_token']

        else:
            return response_data

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.github.v3+json"
        }

        # Get user details
        user_url = f"{base_url}/user"
        user = requests.get(user_url, headers=headers)

        # Get user emails
        if user.status_code == 200:
            user_data = user.json()
            return dict(user_data)
        else:
            return f"IError: {user.status_code}"

    else:
        return f"Error: {response.status_code}"
