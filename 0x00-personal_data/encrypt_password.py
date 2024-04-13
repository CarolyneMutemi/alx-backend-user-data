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
