#!/usr/bin/env python3
"""Module contains the logic for user authentication"""

from typing import Union
import uuid

import bcrypt
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt and returns the hashed password.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    Generates a new UUID and returns it as a string.
    """
    return str(uuid.uuid4())


class Auth:
    """
    The Auth class provides methods for user authentication, including
    registering new users, validating login credentials, and managing
    user sessions.
    """

    def __init__(self):
        """
        Initializes a new Auth instance, which includes a new DB instance.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user with the given email and password.
        If a user with the given email already exists, a ValueError is raised.
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_pwd = _hash_password(password)
            return self._db.add_user(email, hashed_pwd)

        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates the login credentials of a user.
        If the user does not exist or the password is incorrect,
        False is returned.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        hashed_pwd = user.hashed_password
        # if isinstance(hashed_pwd, str):
        #     hashed_pwd = hashed_pwd.encode()

        return bcrypt.checkpw(password.encode(), hashed_pwd)

    def create_session(self, email: str) -> Union[str, None]:
        """
        Creates a new session for the user with the given email.
        If the user does not exist, None is returned.
        """
        try:
            exist_user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        self._db.update_user(exist_user.id, session_id=session_id)

        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[str, None]:
        """
        Retrieves a user from the database using the given session ID.
        If the user does not exist, None is returned.
        """
        if not session_id:
            return None

        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroys the session for the user with the given user ID.
        If the user does not exist, None is returned.
        """
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return

        self._db.update_user(user.id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """
        Generates a reset password token for the user with the given email.
        If the user does not exist, a ValueError is raised.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token = _generate_uuid()

        self._db.update_user(user.id, reset_token=reset_token)

        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Updates the password of the user with the given reset token.
        If the reset token is not valid or the password is not provided,
        a ValueError is raised.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError

        hashed_pwd = _hash_password(password)

        self._db.update_user(
            user.id,
            hashed_password=hashed_pwd,
            reset_token=None
        )
