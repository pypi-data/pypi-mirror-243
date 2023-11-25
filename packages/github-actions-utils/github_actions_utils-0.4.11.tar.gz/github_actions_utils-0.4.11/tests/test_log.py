import tempfile

import pytest

from github_actions_utils.log import github_log_group, summary, summary_exec

from unittest.mock import patch, call


@pytest.fixture
def github_step_summary(monkeypatch):
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        monkeypatch.setenv("GITHUB_STEP_SUMMARY", temp.name)
        yield temp.name


def test_github_log_group_simple(capsys):
    @github_log_group("simple")
    def simple():
        print("Hello, world!")

    simple()
    out, err = capsys.readouterr()
    assert out == "::group::simple\nHello, world!\n::endgroup::\n"
    assert err == ""


def test_github_log_group_using_parameter_value(capsys):
    @github_log_group("$parameter_value")
    def using_parameter_value(parameter_value):
        print(parameter_value)

    using_parameter_value("Hello, world!")
    out, err = capsys.readouterr()
    assert out == "::group::Hello, world!\nHello, world!\n::endgroup::\n"
    assert err == ""


def test_github_log_group_using_parameter_value_with_multiple_parameters(capsys):
    @github_log_group("$parameter_value2 $parameter_value1 $kwarg2 $kwarg1")
    def using_parameter_value_with_multiple_parameters(
            parameter_value1, parameter_value2, kwarg1="default_kwarg", kwarg2="default_kwarg2"
    ):
        print("inside the group")

    using_parameter_value_with_multiple_parameters("Hello,", "world!", kwarg2="KWARG2")
    out, err = capsys.readouterr()
    assert out == "::group::world! Hello, KWARG2 default_kwarg\ninside the group\n::endgroup::\n"
    assert err == ""


def test_github_log_group_using_object_attributes(capsys):
    class TestObject:
        def __init__(self):
            self.attribute = "Hello, world!"

    @github_log_group("$(obj.attribute)")
    def using_object_attributes(obj):
        print(obj.attribute)

    test_object = TestObject()
    using_object_attributes(test_object)
    out, err = capsys.readouterr()
    assert out == "::group::Hello, world!\nHello, world!\n::endgroup::\n"
    assert err == ""


def test_summary_write(github_step_summary):
    summary("Test text", overwrite=False)
    with open(github_step_summary, "r") as f:
        assert f.read() == "Test text\n"


def test_summary_append(github_step_summary):
    summary("Test text", overwrite=False)
    with open(github_step_summary, "r") as f:
        assert f.read() == "Test text\n"

    summary("Test text 2", overwrite=False)
    with open(github_step_summary, "r") as f:
        assert f.read() == "Test text\nTest text 2\n"


def test_summary_overwrite(github_step_summary):
    summary("Test text", overwrite=False)
    with open(github_step_summary, "r") as f:
        assert f.read() == "Test text\n"

    summary("Test text 3", overwrite=True)
    with open(github_step_summary, "r") as f:
        assert f.read() == "Test text 3\n"


def test_summary_exec_success():
    @summary_exec("Test success", lambda r: r)
    def _success():
        return True

    with patch("github_actions_utils.log.summary") as summary_mock:
        resp = _success()
    assert resp is True
    summary_mock.assert_has_calls(
        [
            call("Test success...", end=""),
            call(":white_check_mark:", ),
        ]
    )


def test_summary_exec_fail():
    @summary_exec("Test success", lambda r: r)
    def _success():
        return False

    with patch("github_actions_utils.log.summary") as summary_mock:
        resp = _success()
    assert resp is False
    summary_mock.assert_has_calls(
        [
            call("Test success...", end=""),
            call(":x:", ),
        ]
    )


def test_summary_exec_without_check_true():
    @summary_exec("Test success")
    def _success():
        return True

    with patch("github_actions_utils.log.summary") as summary_mock:
        resp = _success()
    assert resp is True
    summary_mock.assert_has_calls(
        [
            call("Test success...", end=""),
            call(":white_check_mark:", ),
        ]
    )


def test_summary_exec_without_check_false():
    @summary_exec("Test success", False)
    def _success():
        return True

    with patch("github_actions_utils.log.summary") as summary_mock:
        resp = _success()
    assert resp is True
    summary_mock.assert_has_calls(
        [
            call("Test success...", end=""),
            call(":x:", ),
        ]
    )


def test_summary_exec_fail_exception():
    @summary_exec("Test success", lambda r: r)
    def _success():
        raise Exception("error")

    with patch("github_actions_utils.log.summary") as summary_mock:
        with pytest.raises(Exception):
            _success()
    summary_mock.assert_has_calls(
        [
            call("Test success...", end=""),
            call(":x:"),
            call("error"),
        ]
    )
