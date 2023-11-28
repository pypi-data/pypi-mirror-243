from unittest.mock import Mock, patch

import pytest

from github_actions_utils.github import get_github, _extract_owner_and_repo_name, get_commit_message_command

COMMIT_COMMAND_PREFIX = "command"


@pytest.fixture
def repo_mock():
    repo = Mock()
    repo.get_commits.return_value = []
    yield repo


def mock_commit_message(repo, commit_message):
    commit = Mock()
    repo.get_commits.return_value.append(commit)
    commit.commit.message = commit_message


@pytest.fixture
def gh_mock():
    with patch("github.Github") as gh:
        yield gh


@pytest.mark.vcr
def test_get_github_without_token():
    assert get_github().get_user().login == "heitorpolidoro"


@pytest.mark.vcr
def test_get_github_with_token():
    assert get_github("token").get_user().login == "heitorpolidoro"


@pytest.mark.vcr
def test_get_current_repo():
    repo = get_github().get_current_repo()
    assert repo.name == "github_actions_utils"


def test_extract_owner_and_repo_name_with_dot_git():
    owner, repo_name = _extract_owner_and_repo_name(
        "https://github.com/heitorpolidoro/github_actions_utils.git"
    )
    assert repo_name == "github_actions_utils"
    assert owner == "heitorpolidoro"


def test_extract_owner_and_repo_name_without_dot_git():
    owner, repo_name = _extract_owner_and_repo_name(
        "https://github.com/heitorpolidoro/github_actions_utils"
    )
    assert repo_name == "github_actions_utils"
    assert owner == "heitorpolidoro"


def test_get_commit_message_command(repo_mock):
    mock_commit_message(repo_mock, "[command: command]")
    assert get_commit_message_command(repo_mock, COMMIT_COMMAND_PREFIX) == "command"


def test_get_commit_message_with_no_command(repo_mock):
    mock_commit_message(repo_mock, "just a commit")
    assert get_commit_message_command(repo_mock, COMMIT_COMMAND_PREFIX) is None


def test_get_commit_message_command_with_big_message(repo_mock):
    mock_commit_message(repo_mock, "bla" * 1000 + "[command: hidden_command]" + "bla" * 1000)
    assert get_commit_message_command(repo_mock, COMMIT_COMMAND_PREFIX) == "hidden_command"


def test_get_commit_message_command_with_multiple_commands(repo_mock):
    mock_commit_message(repo_mock, "".join(f"[command: command{i}]\n" for i in range(100)))
    assert get_commit_message_command(repo_mock, COMMIT_COMMAND_PREFIX) == "command99"
