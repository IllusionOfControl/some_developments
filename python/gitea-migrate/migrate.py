import os
import re
import json
import time
import tempfile

from loguru import logger
import git
import requests

# Set these variables to match your Gitea and GitHub configurations
GITEA_URL = "http://git.dream.vm:80"
GITEA_TOKEN = "11f5f7ccc5a0f3fadcdcaaa32ecf5460dedd001d"
GITHUB_URL = "https://api.github.com"
GITHUB_TOKEN = "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"

# Regular expression to match Gitea repository URLs
gitea_re = re.compile(r"^http://git\.dream\.vm/([^/]+)/([^/]+)\.git$")

def migrate_repository(gitea_url, github_url):
    # Clone the Gitea repository
    temp_dir = tempfile.TemporaryDirectory()
    repo = git.Repo.clone_from(gitea_url, temp_dir.name, bare=True)

    # Push the repository to GitHub
    repo.delete_remote("origin")
    remote = repo.create_remote("origin", github_url)
    remote.push(mirror=True)

    # Clean up
    temp_dir.cleanup()

def gitea_load_repo_list(token):
    # List the repositories owned by the current user on Gitea
    page = 1
    repos = []
    while True: 
        url = f"{GITEA_URL}/api/v1/user/repos?page={page}&limit=30"
        headers = {"Authorization": f"token {GITEA_TOKEN}"}
        r = requests.get(url, headers=headers)
        repos = [*repos, *r.json()]
        if int(r.headers["x-total-count"]) == len(repos):
            break
        page += 1
    return repos

def github_check_repo_exists(owner, name): 
    url = f"{GITHUB_URL}/repos/{owner}/{name}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", 'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28'}
    r = requests.get(url, headers=headers)
    return r.status_code == 200
        

def github_remove_repo(owner, name):
    url = f"{GITHUB_URL}/repos/{owner}/{name}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", 'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28'}
    r = requests.delete(url, headers=headers)
    r.raise_for_status()

def github_create_new_repo(name, repo):
    data = {
        "name": name,
        "private": repo["private"],
        "description": repo["description"],
    }
    url = f"{GITHUB_URL}/user/repos"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", 'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28'}
    r = requests.post(url, headers=headers, data=json.dumps(data))
    r.raise_for_status()
    return r.json()

def main():
    logger.info("Loading Gitea repository list")
    repos = gitea_load_repo_list(token=GITEA_TOKEN)

    # Iterate over the repositories and migrate them to GitHub
    for repo in repos:
        # Check if the repository URL matches the expected pattern
        m = gitea_re.match(repo["clone_url"])
        if not m:
            continue

        # Get the owner and repository name on Gitea
        owner, name = m.groups()
        owner = "IllusionOfControl"

        # Check if the repository already exists on GitHub
        logger.info(f"Checking repository {name} exists on Github")
        if github_check_repo_exists(owner, name):
            continue
            # logger.info(f"Removing repository {name}")
            # github_remove_repo(owner, name)

        logger.info(f"Creating new repository {name}")
        # Create a new repository on GitHub
        json = github_create_new_repo(name, repo)

        logger.info(f"Migrating repository {name}")
        # Get the clone URL of the new repository on GitHub
        clone_url = json["clone_url"]

        # Migrate the repository from Gitea to GitHub
        migrate_repository(repo["clone_url"], clone_url)

        # Wait 1 second to avoid rate limiting
        time.sleep(1)

if __name__ == "__main__":
    main()
