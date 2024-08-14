#!/usr/bin/env python3

"""
This module provides the DB class for interacting with a SQLite database.
"""

from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """
    The DB class encapsulates a SQLite database connection and provides methods
    for interacting with User records.
    """

    def __init__(self) -> None:
        """
        Initializes a new DB instance. This involves setting up the engine,
        dropping all existing tables, and creating new tables.
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Returns a memoized session object. If no session exists, a new one is
        created and returned.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Adds a new User record to the database with the given email and hashed
        password. The new User object is returned.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()

        return user

    def _validate_attributes(self, kwargs: dict) -> None:
        """
        Validates the given attributes against the User table columns. If any
        invalid keys are found, an InvalidRequestError is raised.
        """
        column_names = User.__table__.columns.keys()
        invalid_keys = [
            key for key in kwargs.keys() if key not in column_names]
        if invalid_keys:
            raise ValueError

    def find_user_by(self, **kwargs) -> User:
        """
        Finds a User record by the given attributes. If no User is found, a
        NoResultFound exception is raised.
        """
        # if not kwargs:
        #     raise InvalidRequestError

        try:
            self._validate_attributes(kwargs)
        except ValueError:
            raise InvalidRequestError

        user = self._session.query(User).filter_by(**kwargs).first()
        if not user:
            raise NoResultFound

        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates a User record with the given user_id and attributes. If the
        User is not found or the attributes are invalid, an exception is
        raised.
        """
        user = self.find_user_by(id=user_id)
        self._validate_attributes(kwargs)

        for key, value in kwargs.items():
            setattr(user, key, value)

        self._session.commit()
