#!/usr/bin/env python3
"""
Creating a session with an expiration duration.
"""
from datetime import datetime, timedelta
import os
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """
    Session authentication with an expiration duration.
    """
    def __init__(self) -> None:
        self.session_duration = os.getenv('SESSION_DURATION', '0')
        if not self.session_duration.isdigit():
            self.session_duration = 0
        self.session_duration = int(self.session_duration)

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a session.
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        if session_id is None or not isinstance(session_id, str):
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        user_id = self.user_id_by_session_id[session_id].get('user_id')
        if self.session_duration <= 0:
            return user_id
        created_at = self.user_id_by_session_id[session_id].get('created_at')
        if created_at is None:
            return None
        expire_time = created_at + timedelta(seconds=self.session_duration)
        if expire_time < datetime.now():
            return None
        return user_id
