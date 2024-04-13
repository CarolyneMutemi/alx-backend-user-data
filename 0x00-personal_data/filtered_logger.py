#!/usr/bin/env python3
"""
Module with filter_datum function.
"""
import os
import re
from typing import List
import logging
from mysql.connector import connection


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


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
    for field in fields:
        message = re.sub(rf"{field}=(.*?){separator}",
                         f"{field}={redaction}{separator}", message)
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


def get_logger() -> logging.Logger:
    """
    Returns a logging.Logger object.
    """
    logger = logging.getLogger('user_data')
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    stream_handler.setLevel(logging.INFO)
    logger.addHandler(stream_handler)
    return logger


def get_db() -> connection.MySQLConnection:
    """
    Returns a connector to the database
    """
    credentials = {
        "user": os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        'password': os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        'host': os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        'database': os.getenv('PERSONAL_DATA_DB_NAME')
    }
    connector = connection.MySQLConnection(**credentials)
    return connector
