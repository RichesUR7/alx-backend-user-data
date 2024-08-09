#!/usr/bin/env python3
"""
A UserSession represents a session of a user in the application.
"""

from models.base import Base


class UserSession(Base):
    """A class used to represent a UserSession."""

    def __init__(self, *args: list, **kwargs: dict):
        """Initializes the UserSession with the user ID and session ID."""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id")
        self.session_id = kwargs.get("session_id")
