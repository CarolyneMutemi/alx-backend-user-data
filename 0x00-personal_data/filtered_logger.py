#!/usr/bin/env python3
"""
Module with filter_datum function.
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Logs message obfuscated."""
    for data in message.split(separator):
        if data.split('=')[0] in fields:
            message = re.sub(data.split('=')[1], redaction, message)
    return message
