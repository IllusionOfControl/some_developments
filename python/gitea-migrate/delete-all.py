import os
import re
import json
import time
import tempfile

from loguru import logger
import git
import requests

GITHUB_URL = "https://api.github.com"
GITHUB_TOKEN = "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"

def github_get_user():
    url = f"{GITHUB_URL}/user"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", 'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28'}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()

def github_get_all_repos():
    url = f"{GITHUB_URL}/user/repos?per_page=30&page=1"
    repos = []
    while True:
        headers = {"Authorization": f"token {GITHUB_TOKEN}", 'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28'}
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        repos = [*repos, *r.json()]
        if r.links.get('next'):
            url = r.links['next']['url']
        else:
            return repos

def github_remove_repo(owner, name):
    url = f"{GITHUB_URL}/repos/{owner}/{name}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", 'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28'}
    r = requests.delete(url, headers=headers)
    r.raise_for_status()

def main():
    logger.info("Getting User Profile")
    owner = github_get_user()['login']
    logger.info("Getting User Repos")
    repos = github_get_all_repos()
    logger.info(f"Repos found: {len(repos)}")

    for repo in repos:
        logger.info(f"Removing repo: {repo['name']}")
        github_remove_repo(owner, repo['name'])

    logger.info(f"Repos removed: {len(repos)}")


if __name__ == "__main__":
    main()