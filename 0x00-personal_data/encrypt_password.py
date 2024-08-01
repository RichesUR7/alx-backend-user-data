#!/usr/bin/env python3
"""
Module for hashing and validating passwords.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Generate a salted, hashed password.

    Args:
        password (str): The plain text password to hash.

    Returns:
        bytes: The salted, hashed password as a byte string.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)

    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validate that the provided password matches the hashed password.

    Args:
        hashed_password (bytes): The hashed password.
        password (str): The plain text password to validate.

    Returns:
        bool: True if the password matches the hashed password,False otherwise.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
