#!/usr/bin/env python3
"""
A module to apply authorization logic.
"""

import fnmatch
from typing import List, TypeVar

from flask import request

User = TypeVar("User")


class Auth:
    """[TODO:description]"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Returns False if path is in the list of excluded paths"""
        if path is None:
            return True

        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        # Add trailing slash for comparison
        if not path.endswith("/"):
            path += "/"

        for pattern in excluded_paths:
            if fnmatch.fnmatch(path, pattern):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Return the value of the header request Authorization"""
        if request is None:
            return None

        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> User:
        """The Method is returning None for now"""
        return None
