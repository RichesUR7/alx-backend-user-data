#!/usr/bin/env python3
"""Module contains the logic for auth session expiration"""

import os
from datetime import datetime, timedelta

from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """A class that handles session expiration authentication."""

    def __init__(self):
        """
        Initializes the SessionExpAuth with the session duration.
        """
        self.session_duration = int(os.getenv("SESSION_DURATION", 0))

    def create_session(self, user_id=None):
        """Creates a new session for a user."""
        session_id = super().create_session(user_id)
        if session_id:
            self.user_id_by_session_id[session_id] = {
                "user_id": user_id,
                "created_at": datetime.now(),
            }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieves the user_id associated with a session_id."""
        if session_id:
            user_details = self.user_id_by_session_id.get(session_id)
            if user_details and "created_at" in user_details:
                if (
                    self.session_duration <= 0
                    or user_details["created_at"]
                    + timedelta(seconds=self.session_duration)
                    >= datetime.now()
                ):
                    return user_details.get("user_id")
        return None
