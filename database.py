import sqlite3
import logging
from objects import *

logger = logging.getLogger(__name__)

DEFAULT_FILE_PATH = "./database.db"
db_file_path = DEFAULT_FILE_PATH

INITIAL_STATEMENTS = [
    """CREATE TABLE IF NOT EXISTS users (
            uuid TEXT PRIMARY KEY, 
            name TEXT NOT NULL,
            password_hash TEXT NOT NULL
        );""",

    """CREATE TABLE IF NOT EXISTS posts (
            uuid TEXT PRIMARY KEY, 
            content TEXT NOT NULL, 
            owner TEXT NOT NULL, 
            comments TEXT NOT NULL, 
            impostors TEXT NOT NULL, 
            innocents TEXT NOT NULL
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

def get_posts(connection: sqlite3.Connection) -> list[Post]:
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM posts")
    rows = cursor.fetchall()
    return [
        Post(
            uuid=UUID(row[0]),
            content=row[1],
            owner=getUser(connection, UUID(row[2])),
            comments=row[3].split(",") if row[3] else [],
            roles={}
        )
        for row in rows
    ]

def getUser(connection: sqlite3.Connection, user_uuid: UUID) -> User | None:
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE uuid = ?", (str(user_uuid),))
    row = cursor.fetchone()
    if row:
        return User(uuid=UUID(row[0]), name=row[1], password_hash=row[2])
    return None