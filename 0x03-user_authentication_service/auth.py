#!/usr/bin/env python3
"""
Auth module.
"""

import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """
    Takes in a password string and returns a salted harsh of it.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    Returns a string representation of a new UUID.
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register as user and returns the User instance.
        """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f'User {user.email} already exists')
        except NoResultFound:
            password = _hash_password(password)
            user = self._db.add_user(email, password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates a user's credentials.
        """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode(), user.hashed_password):
                return True
            return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        Takes an email string argument and returns the session ID as a string.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user_id=user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        It takes a single session_id string argument
        and returns the corresponding User or None.
        """
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Updates the corresponding user's session ID to None.
        """
        try:
            user = self._db.find_user_by(id=user_id)
            user.session_id = None
            return
        except NoResultFound:
            return

    def get_reset_password_token(self, email: str) -> str:
        """
        Generates a reset password token.
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = str(uuid4())
            user.reset_token = reset_token
            return reset_token
        except NoResultFound as error:
            raise ValueError from error

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Updates password.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            user.hashed_password = _hash_password(password)
            user.reset_token = None
            return
        except NoResultFound as error:
            raise ValueError from error
