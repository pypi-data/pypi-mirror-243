import os
from typing import Any

type_ = type


def str_to_bool(s):
    return s.lower() in ['true', '1', 't', 'y', 'yes']


# noinspection PyShadowingBuiltins
def get_env(env: str, default: Any = None, type: type_ = None) -> Any:
    value = os.getenv(env, default)
    if type is not None:
        if type == bool:
            value = str_to_bool(value)
        else:
            value = type(value)
    return value


# noinspection PyShadowingBuiltins
def get_github_env(env: str, default: Any = None, type: type_ = None) -> Any:
    return get_env(f'GITHUB_{env}', default, type)


# noinspection PyShadowingBuiltins
def get_input(env: str, default: Any = None, type: type_ = None) -> Any:
    return get_env(f'INPUT_{env}', default, type)


class GithubEnvs:
    def __getattr__(self, item):
        return get_github_env(item.upper())


class Inputs:
    def __getattr__(self, item):
        return get_input(item.upper())


github_envs = GithubEnvs()
inputs = Inputs()
