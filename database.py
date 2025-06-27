import sqlite3
import logging

logger = logging.getLogger(__name__)

DEFAULT_FILE_PATH = "./database.db"
db_file_path = DEFAULT_FILE_PATH

INITIAL_STATEMENTS = [
    """CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY, 
            name text NOT NULL, 
            begin_date DATE, 
            end_date DATE
        );""",

    """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY, 
            name TEXT NOT NULL, 
            priority INT, 
            project_id INT NOT NULL, 
            status_id INT NOT NULL, 
            begin_date DATE NOT NULL, 
            end_date DATE NOT NULL, 
            FOREIGN KEY (project_id) REFERENCES projects (id)
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

