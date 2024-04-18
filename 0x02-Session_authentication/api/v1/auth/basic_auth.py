#!/usr/bin/env python3
"""
Basic auth.
"""
import base64
import binascii
import re
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User
from models.base import DATA


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
        Returns the decoded value of a Base64 string
        base64_authorization_header.
        """
        if not base64_authorization_header or not isinstance(
                base64_authorization_header, str):
            return None
        try:
            decoded_string = base64.b64decode(base64_authorization_header)
        except binascii.Error:
            return None
        try:
            decoded = decoded_string.decode('utf-8')
        except UnicodeDecodeError:
            return None
        return decoded

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
        data = decoded_base64_authorization_header.split(':', 1)
        return (data[0], data[1])

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        Returns the User instance based on their email and password.
        """
        if not user_email or not isinstance(user_email, str):
            return None
        if not user_pwd or not isinstance(user_pwd, str):
            return None
        if len(DATA) == 0:
            return None
        user_list = User.search({'email': user_email})
        if len(user_list) == 0:
            return None
        for user in user_list:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves user instance for a request.
        """
        header = self.authorization_header(request)
        base64_string = self.extract_base64_authorization_header(header)
        decoded_data = self.decode_base64_authorization_header(base64_string)
        email_password = self.extract_user_credentials(decoded_data)
        user = self.user_object_from_credentials(email_password[0],
                                                 email_password[1])
        return user
