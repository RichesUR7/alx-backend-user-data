#!/usr/bin/env python3
"""
This module applies session authentication logic.
"""
from uuid import uuid4
from models.user import User
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """
    A class used to manage session-based user authentication.

    Attributes
    ----------
    user_id_by_session_id : dict
        A dictionary that maps session IDs (str) to user IDs (str).
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a new session for a user."""
        if user_id is None or not isinstance(user_id, str):
            return None

        gen_id = uuid4()
        self.user_id_by_session_id[str(gen_id)] = user_id
        return str(gen_id)

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Get the user id from the session."""
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Get a User based on his session ID."""
        cookie_value = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cookie_value)
        curr_user = User.get(user_id)
        return curr_user

    def destroy_session(self, request=None):
        """Deletes a user session."""
        if request:
            cookie_value = self.session_cookie(request)
            user_id = self.user_id_for_session_id(cookie_value)
            if cookie_value and user_id:
                del self.user_id_by_session_id[cookie_value]
                return True
        return False
