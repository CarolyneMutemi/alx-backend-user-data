#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound, InvalidRequestError
from user import User

from user import Base


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Adds a user to the database and returns a User object.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self.__session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Takes in arbitrary keyword arguments
        and returns the first row found in the users table
        as filtered by the method's input arguments.
        """
        session = self._session
        for key, item in kwargs.items():
            if key not in User.__dict__:
                raise InvalidRequestError
            result = session.query(User).filter(eval(f'User.{key}')
                                                == item).first()
            if not result:
                raise NoResultFound
            return result
        raise InvalidRequestError
