#!/usr/bin/env python3
"""
Auth module.
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Takes in a password string and returns a salted harsh of it.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
