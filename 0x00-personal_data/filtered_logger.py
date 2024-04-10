#!/usr/bin/env python3
"""
Module with filter_datum function.
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Logs message obfuscated.
    Args:
        fields -  a list of strings representing all fields to obfuscate.
        redaction - a string representing by what the field will be obfuscated.
        message - a string representing the log line.
        separator - a string representing by which character
        is separating all fields in the message.
    Return:
        The log message string is returned with the obfuscated fields.
    """
    for data in message.split(separator):
        key_value = data.split('=')
        if key_value[0] in fields:
            message = re.sub(key_value[1], redaction, message)
    return message
