#!/usr/bin/env python3
"""
API authentication.
"""
from flask import request
from typing import List, TypeVar
import re
import os


class Auth:
    """
    Manages API aunthentication.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Returns a True if path requires auth, i.e, is not in excluded_paths
        otherwise, returns False.
        """
        if excluded_paths is None or path is None:
            return True
        if path[-1] != '/':
            path += '/'
        for excluded_path in excluded_paths:
            pattern = excluded_path.replace('*', '.*')
            if re.search(pattern, path):
                return False
        if path not in excluded_paths:
            return True
        print("Past")
        return False

    def authorization_header(self, request=None) -> str:
        """
        Returns the authorization header.
        """
        header = request.headers.get('Authorization', None)
        if request is None or header is None:
            return None
        return header

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Current user.
        """
        return None

    def session_cookie(self, request=None):
        """
        Returns the cookie value from a request.
        """
        if not request:
            return None
        cookie_name = os.getenv('SESSION_NAME')
        return request.cookies.get(cookie_name)
