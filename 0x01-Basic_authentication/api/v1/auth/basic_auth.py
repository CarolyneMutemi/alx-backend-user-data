#!/usr/bin/env python3
"""
Basic auth.
"""
from api.v1.auth.auth import Auth
import re


class BasicAuth(Auth):
    """
    Basic authentication.
    """
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        EXtracts the base64 part of the authorization header.
        """
        if authorization_header is None or not isinstance(authorization_header, str):
            return None
        if re.search(r"^Basic ", authorization_header) is None:
            return None
        return authorization_header.split(' ')[1]
