from unittest.mock import Mock

import pytest

from github_actions_utils.git import get_gh_repo, _extract_owner_and_repo_name, get_commit_message_command

COMMIT_COMMAND_PREFIX = "command"


@pytest.fixture(scope="module")
def vcr_cassette_name(request):
    return "get_repo.yaml"


@pytest.fixture(autouse=True)
def clear_lru_cache():
    yield
    get_gh_repo.cache_clear()


@pytest.fixture
def repo():
    yield get_gh_repo()


@pytest.fixture
def repo_mock():
    repo = Mock()
    repo.get_commits.return_value = []
    yield repo


def mock_commit_message(repo, commit_message):
    commit = Mock()
    repo.get_commits.return_value.append(commit)
    commit.commit.message = commit_message


@pytest.mark.vcr
def test_get_gh_repo(repo):
    assert repo.name == "github_actions_utils"
    assert repo.owner.login == "heitorpolidoro"


@pytest.mark.vcr
def test_get_gh_repo_token(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "github_token")
    repo = get_gh_repo()
    assert repo.name == "github_actions_utils"
    assert repo.owner.login == "heitorpolidoro"


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
