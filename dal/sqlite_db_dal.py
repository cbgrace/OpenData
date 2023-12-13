import sqlite3
from contextlib import contextmanager
from config import DATABASE_PATH
from logging_config import get_logger
from exceptions.custom_exceptions import DalException

"""
This module contains functions built to establish a connection with a database, query that database, and return the 
results of that query. 

Methods:
--------
    get_connection():
        attempts to establish a connection with the database located at DATABASE_PATH (imported from config)
    get_cursor(connection):
        creates a cursor for the connection from get_connection()
    close_connection(connection):
        closes the connection.
    execute(query, params=None):
        attempts to execute a query, with optional params, using get_connection() and get_cursor().
"""

logger = get_logger(__name__)


@contextmanager
def get_connection():
    """
    attempts to open a connection with the database at DATABASE_PATH, if successful, it yields that connection,
    if not, it returns an error & logs that error.
    :return: yields the connection (if successful)
    """
    connection = None
    try:
        connection = sqlite3.connect(DATABASE_PATH)
        logger.info(f"Connected to database at {DATABASE_PATH}")
        yield connection
    except sqlite3.Error as e:
        logger.error(f"Failed to get a connection, Error: {e}")
        raise
    finally:
        if connection:
            connection.close()


@contextmanager
def get_cursor(connection):
    """
    establishes a cursor for the connection created by get_connection()
    :param connection: the connection created by get_connection
    :return: yields the cursor
    """
    cursor = connection.cursor()
    try:
        yield cursor
    finally:
        cursor.close()


def close_connection(connection):  # I don't think I need this.
    """
    method to close the connection
    :param connection: the specific connection to close
    :return: no return, just closes the connection using the .close() method, and logs that the database is closed.
    """
    if connection:
        connection.close()
        logger.info("Database connection closed.")


def execute(query, params=None):
    """
    attempts to execute a query, with optional params, using get_connection() and get_cursor().
    :param query: the query you would like to execute
    :param params: optional parameters for said query.
    :return: returns cursor.fetchall(), a.k.a. all the results of the successful query.
    """
    try:
        logger.info(f"Query of {query} params {params}")
        with get_connection() as connection:
            with get_cursor(connection) as cursor:
                if params is not None:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                connection.commit()
                logger.info(f"Query was successful {query}")
                return cursor.fetchall()
    except sqlite3.Error as e:
        logger.error(f"Database error {e} with query {query} params {params}")
        raise DalException(f"Error with query {query} caused by {e}")