""" Module for database engine """

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

def get_engine() -> str:
    """ Get engine for database connection """

    load_dotenv()

    DB_NAME = os.getenv('DB_NAME')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_PWD = os.getenv('DB_PWD')
    DB_USER = os.getenv('DB_USER')

    connection_string=f"postgresql+psycopg://{DB_USER}:{DB_PWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    return create_engine(connection_string)
