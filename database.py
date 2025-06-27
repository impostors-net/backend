import sqlite3
import logging

logger = logging.getLogger(__name__)

DEFAULT_FILE_PATH = "./database.db"
db_file_path = DEFAULT_FILE_PATH

INITIAL_STATEMENTS = [
    """CREATE TABLE IF NOT EXISTS users (
            uuid TEXT PRIMARY KEY, 
            name TEXT NOT NULL
        );""",

    """CREATE TABLE IF NOT EXISTS posts (
            uuid TEXT PRIMARY KEY, 
            content TEXT NOT NULL, 
            owner TEXT NOT NULL
        );""",

    """CREATE TABLE IF NOT EXISTS comments (
            uuid TEXT PRIMARY KEY, 
            content TEXT NOT NULL,
            owner TEXT NOT NULL, 
            post TEXT NOT NULL
        );"""
]


def main(connection: sqlite3.Connection):

    cursor = connection.cursor()

    for statement in INITIAL_STATEMENTS:
        cursor.execute(statement)

    connection.commit()

def start() -> sqlite3.Connection | None:
    try:
        conn = sqlite3.connect(db_file_path)
        logging.debug(f"Opened SQLite database {db_file_path} with version {sqlite3.sqlite_version} successfully.")
        return conn

    except sqlite3.OperationalError as e:
        logger.fatal("Failed to open database:", e)
        return None

