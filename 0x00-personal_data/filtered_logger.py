#!/usr/bin/env python3
"""
Module for filtering Personally Identifiable Information (PII) in logs.
"""
import logging
import os
import re
from typing import List

import mysql.connector
from mysql.connector.cursor import MySQLCursorDict


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """
    Obfuscates PII fields in a log message.

    Args:
        fields (List[str]): List of PII fields to obfuscate.
        redaction (str): The string to replace PII fields with.
        message (str): The log message containing PII.
        separator (str): The separator used in the log message.

    Returns:
        str: The obfuscated log message.
    """
    for field in fields:
        message = re.sub(
            f"{field}=.+?{separator}",
            f"{field}={redaction}{separator}",
            message
        )
    return message


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class for obfuscating PII in logs.
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the RedactingFormatter.

        Args:
            fields (List[str]): List of PII fields to obfuscate.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record, obfuscating PII fields.

        Args:
            record (logging.LogRecord): The log record.

        Returns:
            str: The formatted log record with obfuscated PII fields.
        """
        return filter_datum(
            self.fields, self.REDACTION,
            super().format(record), self.SEPARATOR
        ).rstrip(self.SEPARATOR) + self.SEPARATOR


def get_logger() -> logging.Logger:
    """
    Creates and configures a logger for user data with PII redaction.

    Returns:
        logging.Logger: Configured logger with redaction formatter.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(list(PII_FIELDS))
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Establishes a connection to the database.

    Returns:
        Database connection object.
    """
    connection = mysql.connector.connection.MySQLConnection(
        user=os.environ.get("PERSONAL_DATA_DB_USERNAME", "root"),
        password=os.environ.get("PERSONAL_DATA_DB_PASSWORD", ""),
        host=os.environ.get("PERSONAL_DATA_DB_HOST", "localhost"),
        database=os.environ.get("PERSONAL_DATA_DB_NAME"),
        port=3306
    )

    return connection


def main() -> None:
    """
    Obtain a database connection using get_db and retrieve all rows
    in the users table and display each row under a filtered format
    """
    db_connection = get_db()
    cursor: MySQLCursorDict = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users;")
    logger = get_logger()

    for row in cursor:
        log_message = "; ".join(f"{key}={value}" for key, value in row.items())
        logger.info(log_message)

    cursor.close()
    db_connection.close()


if __name__ == "__main__":
    main()
