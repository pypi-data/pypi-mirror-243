from github_actions_utils.env import get_env, get_github_env, github_envs, get_input, inputs


def test_get_env(monkeypatch):
    monkeypatch.setenv("TEST_ENV", "test")
    assert get_env("TEST_ENV") == "test"


def test_get_env_not_existing():
    assert get_env("TEST_ENV") is None


def test_get_env_default():
    assert get_env("TEST_ENV", "default") == "default"


def test_get_env_type_cast(monkeypatch):
    monkeypatch.setenv("TEST_ENV", "42")
    assert get_env("TEST_ENV", type=int) == 42


def test_get_env_type_bool_true(monkeypatch):
    monkeypatch.setenv("TEST_ENV", "true")
    assert get_env("TEST_ENV", type=bool) is True


def test_get_env_type_bool_false(monkeypatch):
    monkeypatch.setenv("TEST_ENV", "False")
    assert get_env("TEST_ENV", type=bool) is False


def test_github_env(monkeypatch):
    monkeypatch.setenv("GITHUB_ENV", "test")
    assert get_github_env("ENV") == "test"


def test_github_env_class(monkeypatch):
    monkeypatch.setenv("GITHUB_ENV", "test")
    assert github_envs.env == "test"


def test_input_env(monkeypatch):
    monkeypatch.setenv("INPUT_ENV", "test")
    assert get_input("ENV") == "test"


def test_input_env_class(monkeypatch):
    monkeypatch.setenv("INPUT_ENV", "test")
    assert inputs.env == "test"
