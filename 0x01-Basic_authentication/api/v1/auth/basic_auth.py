#!/usr/bin/env python3
"""
Basic auth.
"""
import base64
import re
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    Basic authentication.
    """
    def extract_base64_authorization_header(self,
                                            authorization_header:
                                            str) -> str:
        """
        EXtracts the base64 part of the authorization header.
        """
        if authorization_header is None or not isinstance(
                authorization_header, str):
            return None
        if re.search(r"^Basic ", authorization_header) is None:
            return None
        return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """
        Returns the decoded value of a Base64 string base64_authorization_header.
        """
        if not base64_authorization_header or not isinstance(
                base64_authorization_header, str):
            return None
        try:
            decoded_string = base64.b64decode(base64_authorization_header)
        except:
            return None
        return decoded_string.decode('utf-8')
    
    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """
        Returns the user email and password from the Base64 decoded value.
        """
        if not decoded_base64_authorization_header or not isinstance(
                decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        data = decoded_base64_authorization_header.split(':')
        return (data[0], data[1])
