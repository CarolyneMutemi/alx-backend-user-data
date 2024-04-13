#!/usr/bin/env python3
"""
Encrypting passwords using bycrypt.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Returns a salted, hashed password.
    """
    return bcrypt.hashpw(str.encode(password), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates the provided password matches the hashed password.
    """
    return bcrypt.checkpw(str.encode(password), hashed_password)
