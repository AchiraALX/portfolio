#!/usr/bin/env python3
"""This is the GitHub API script
"""
from github import Github
import requests
from urllib.parse import urlencode
import json
import mistune
import getpass

# Get the local host name
local = getpass.getuser()

# GitHub OAuth app credentials
file_dir = f"/home/{local}/token.json"
with open(file_dir) as f:
    admin_data = json.load(f)

client_id = admin_data["client_id"]
client_secret = admin_data["client_secret"]
app_id = admin_data["app_id"]
app_secret = admin_data["app_secret"]
redirect_uri = "https://www.blissprism.tech"
scope = "user:email,repo"

# Create a GitHub instance
def github_instance(token):
    """GitHub instance

    Returns:
        object: GitHub instance
    """
    if token:
        g = Github(token)
    else:
        g = Github()

    return g

# Get the github username
def get_username(token):
    """Get username
    """

    g = github_instance(token)
    username = g.get_user().login

    return username

def get_repo_details(token, name, username):
    """Get repo details

    Args:
        name (str): Repository name

    Returns:
        dict: Repository details
    """

    g = github_instance(token)

    try:
        repo = g.get_repo(f"{username}/{name}")
        read_me = repo.get_readme().decoded_content.decode()
        read_me = mistune.markdown(read_me)
        return {
            "name": repo.name,
            "description": repo.description,
            "stars": repo.stargazers_count,
            "followers": repo.get_contributors().totalCount,
            "readme": read_me,
            "languages": repo.get_languages(),
            "files": repo.get_contents(""),
            'url': repo.html_url,
        }

    except Exception as e:
        return {
            "error": "Repository not found"
        }

def git_all_repos(token):
    """Get repos

    Returns:
        list: List of repos
    """
    g = github_instance(token)
    user = g.get_user()

    try:
        repos = []
        for repo in g.get_user().get_repos():
            details = {
                "repositoryName": repo.name,
                "repositoryUrl": repo.html_url
            }
            repos.append(details)

    except Exception as e:
        return {
            "error": "Invalid tk"
        }

    return repos

# Get the special readme
def get_special_repo(token):
    """Fishes the user readme description
    """

    g = github_instance(token)
    try:
        for repo in g.get_user().get_repos():
            if repo.name == get_username(token):
                name = repo.name
                username = get_username(token)
                repo = get_repo_details(token, name, username)
                return repo

    except Exception as e:
        return {
            "error": "Invalid tk"
        }

# Get GitHub authorization url
def get_auth_url():
    """Get authorization url
    """
    return 'https://github.com/login/oauth/authorize?' + urlencode({
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'scope': scope
    })



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


#
# Jacob Achira
#