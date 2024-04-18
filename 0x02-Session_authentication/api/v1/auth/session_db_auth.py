#!/usr/bin/env python3
"""
Saving sessions in database.
"""
from datetime import datetime, timedelta
from uuid import uuid4
from models.user_session import UserSession
from api.v1.auth.session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """
    Saves sessions in the database.
    """
    def create_session(self, user_id: str = None) -> str:
        """
        Create a session.
        """
        if not user_id or not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        new_session = UserSession()
        new_session.user_id = user_id
        new_session.session_id = session_id
        new_session.save()
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieve user_id from database.
        """
        if not session_id or not isinstance(session_id, str):
            return None
        user_session_list = UserSession.search({'session_id': session_id})
        if len(user_session_list) == 0:
            return None
        user_session = user_session_list[0]
        if self.session_duration <= 0:
            return user_session.user_id
        created_at = user_session.created_at
        if created_at is None:
            return None
        expire_time = created_at + timedelta(seconds=self.session_duration)
        if expire_time < datetime.now():
            return None
        return user_session.user_id
    
    def destroy_session(self, request=None):
        """
        Destroys a session.
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        if not self.user_id_for_session_id(session_id):
            return False
        user_session_list = UserSession.search({'session_id': session_id})
        if len(user_session_list) == 0:
            return False
        UserSession.remove(user_session_list[0])
        return True
