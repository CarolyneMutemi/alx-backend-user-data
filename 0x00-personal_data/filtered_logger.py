#!/usr/bin/env python3
"""
Module with filter_datum function.
"""
import re
from typing import List
import logging
import time


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


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Filters values in incoming log records.
        """
        record.message = filter_datum(self.fields, self.REDACTION,
                                      record.getMessage(),
                                      self.SEPARATOR)
        result = self.FORMAT % {"name": record.name,
                                "levelname": record.levelname,
                                "asctime": self.formatTime(record),
                                "message": record.message
                                }
        return result
