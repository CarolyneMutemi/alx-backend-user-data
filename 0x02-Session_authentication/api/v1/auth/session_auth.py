#!/usr/bin/python3
"""
Session authentication.
"""
from uuid import uuid4
from api.v1.auth.auth import Auth
from models.base import DATA
from models.user import User


class SessionAuth(Auth):
    """
    Session authentication.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a session id for a user_id.
        """
        if not user_id or not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns a User ID based on a Session ID:
        """
        if not session_id or not isinstance(session_id, str):
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Returns a User instance based on a cookie value.
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if len(DATA) == 0:
            return None
        return User.get(user_id)

    def destroy_session(self, request=None):
        """
        Deletes a user session.
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        if not self.user_id_for_session_id(session_id):
            return False
        del SessionAuth.user_id_by_session_id[session_id]
        return True
