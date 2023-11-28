# -*- coding: utf-8 -*-
"""Evironment variable utils."""

import os
from typing import Optional


class MissingEnvironmentVariable(Exception):
    """Raised when an environment variable is missing."""

    def __init__(self, variable_name: str):
        """Initialize."""
        super().__init__(f"Environment variable `{variable_name}` is missing.")


def get_env(variable_name: str, default_value: Optional[str] = None) -> str:
    """
    Get environment variable if it exists.

    Raises
    ------
        MissingEnvironmentVariable
    """
    env_var = os.getenv(variable_name)
    if os.getenv(variable_name) is not None:
        return str(env_var)
    if default_value is not None:
        return default_value

    raise MissingEnvironmentVariable(variable_name)
