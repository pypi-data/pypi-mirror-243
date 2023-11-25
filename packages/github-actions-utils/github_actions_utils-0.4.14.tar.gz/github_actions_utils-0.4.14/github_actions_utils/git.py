import os
import re
from functools import lru_cache
from typing import Tuple

from git import Repo
from github import Github
from github.Auth import Token
from github.Repository import Repository


def _extract_owner_and_repo_name(remote_url: str) -> Tuple[str, str]:
    """
    Extract the owner and repository name from the URL
    :param remote_url: The url to extract the owner and the repo name
    :return: A tuple with the owner and the repo name
    """
    owner, repo_name = remote_url.split("/")[-2:]
    # Remove '.git' from the repo_name if it's there
    if repo_name.endswith(".git"):
        repo_name = repo_name[:-4]
    return owner, repo_name


@lru_cache
def get_gh_repo(token: str = None) -> Repository:
    """
    Return s a GitHub repository object.
    :param token: The github token, optional
    :return: A Github.Repository object
    """
    token = token or os.getenv("GITHUB_TOKEN")
    if token:
        gh = Github(auth=Token(token))
    else:
        gh = Github()
    repo = Repo(os.getcwd())
    # Get the URL of the 'origin' remote
    remote_url = repo.remotes.origin.url

    owner, repo_name = _extract_owner_and_repo_name(remote_url)

    return gh.get_repo(f"{owner}/{repo_name}")


def get_commit_message_command(repo: Repository, command_prefix: str) -> str | None:
    """
    Retrieve the command from the last commit message.
    The command in the commit message must be in the format [command_prefix: command]

    :param repo: The repository object.
    :param command_prefix: The command prefix to look for in the commit message.
    :return: The extracted command or None if there is no command.
    :raises: ValueError if the command is not valid.
    """
    commit_message = repo.get_commits()[0].commit.message
    command_pattern = rf'\[{command_prefix}:(.+?)\]'
    commands_found = re.findall(command_pattern, commit_message)
    if commands_found:
        return commands_found[-1].strip()
    return None
