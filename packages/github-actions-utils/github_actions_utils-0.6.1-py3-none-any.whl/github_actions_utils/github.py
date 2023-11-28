import re
import subprocess
from functools import lru_cache

from github import Github
from github.Auth import Token
from github.Repository import Repository

from github_actions_utils.env import github_envs


def _extract_owner_and_repo_name(remote_url: str) -> tuple[str, str]:
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


class GithubPlus(Github):
    def get_current_repo(self) -> Repository:
        """
        :return: A Github.Repository object for the current directory
        """
        # repo = Repo()
        # remote_url = repo.remotes.origin.url

        remote_url = subprocess.check_output(["git", "config", "--get", "remote.origin.url"])

        owner, repo_name = _extract_owner_and_repo_name(remote_url.decode().strip())

        return self.get_repo(f"{owner}/{repo_name}")


@lru_cache
def get_github(token: str = None) -> GithubPlus:
    """
    Returns an logged instance of Github.
    If token is not provided, it will try to get the token from the environment.
    If the token is not found, it will return an unlogged instance of Github.
    If the token is found, it will return an logged instance of Github.
    :param token: The token to use to log in. If not provided, it will try to get the token from the environment.
    :return: An instance of Github.
    """
    token = token or github_envs.token
    token = Token(token) if token else None
    gh = GithubPlus(auth=token)
    return gh


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
    command_pattern = rf"\[{command_prefix}:(.+?)\]"
    commands_found = re.findall(command_pattern, commit_message)
    if commands_found:
        return commands_found[-1].strip()
    return None
